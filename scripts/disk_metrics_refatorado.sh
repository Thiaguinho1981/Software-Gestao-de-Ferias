#!/bin/bash

# Coletor de métricas SMART/RAID para discos atrás de controladora cciss.
# Uso: ./disk_metrics_refatorado.sh <DEV> <ID> <METRIC>
# Ex.: ./disk_metrics_refatorado.sh sda 1 temp

set -u

SMARTCTL="${SMARTCTL:-/usr/sbin/smartctl}"
SSACLI="${SSACLI:-/usr/sbin/ssacli}"
CTRL_SLOT="${CTRL_SLOT:-0}"

log_error() {
  printf '[%s] %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$*" >&2
}

die() {
  log_error "$*"
  echo -1
  exit 1
}

map_bay() {
  case "$1" in
    0) echo "1I:1:1" ;;
    1) echo "1I:1:2" ;;
    2) echo "1I:1:3" ;;
    3) echo "1I:1:4" ;;
    *) echo "" ;;
  esac
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "Comando não encontrado: $1"
}

if [ "$#" -ne 3 ]; then
  die "Uso inválido. Esperado: <DEV> <ID> <METRIC>"
fi

DEV="$1"
ID="$2"
METRIC="$3"
BAY="$(map_bay "$ID")"

case "$ID" in
  ''|*[!0-9]*) die "ID deve ser numérico" ;;
esac

case "$METRIC" in
  health|temp|defects|reallocated|pending|uncorrect|poweron|wear|status) ;;
  *) die "Métrica inválida: $METRIC" ;;
esac

require_cmd "$SMARTCTL"
if [ "$METRIC" = "status" ]; then
  require_cmd "$SSACLI"
fi

OUT="$(sudo "$SMARTCTL" -a -d cciss,"$ID" "/dev/$DEV" 2>/dev/null || true)"
if [ -z "$OUT" ] && [ "$METRIC" != "status" ]; then
  die "Falha ao coletar SMART de /dev/$DEV (id $ID)"
fi

case "$METRIC" in
  health)
    if sudo "$SMARTCTL" -H -d cciss,"$ID" "/dev/$DEV" 2>/dev/null | grep -Eiq 'OK|PASSED'; then
      echo 0
    else
      echo 1
    fi
    ;;

  temp)
    TEMP="$(printf '%s\n' "$OUT" | awk '
      /Current Drive Temperature/ {print $4; exit}
      /Temperature_Celsius/ {print $10; exit}
      /Temperature:/ {print $2; exit}
    ')"
    echo "${TEMP:-0}"
    ;;

  defects|reallocated)
    DEFECTS="$(printf '%s\n' "$OUT" | awk '
      /Elements in grown defect list/ {print $6; exit}
      /Reallocated_Sector_Ct/ {print $10; exit}
      /Reallocated Event Count/ {print $4; exit}
    ')"
    echo "${DEFECTS:-0}"
    ;;

  pending)
    PENDING="$(printf '%s\n' "$OUT" | awk '
      /Current_Pending_Sector/ {print $10; exit}
      /pending/i {print $NF; exit}
    ')"
    echo "${PENDING:-0}"
    ;;

  uncorrect)
    UNCORRECT="$(printf '%s\n' "$OUT" | awk '
      /Offline_Uncorrectable/ {print $10; exit}
      /Reported_Uncorrect/ {print $10; exit}
      /uncorrected/ {print $NF; exit}
    ')"
    echo "${UNCORRECT:-0}"
    ;;

  poweron)
    POWERON="$(printf '%s\n' "$OUT" | awk '
      /Accumulated power on time/ {
        split($6,a,":");
        print a[1];
        exit
      }
      /Power_On_Hours/ {print $10; exit}
    ')"
    echo "${POWERON:-0}"
    ;;

  wear)
    WEAR_RAW="$(printf '%s\n' "$OUT" | awk '
      /Media_Wearout_Indicator/ {print $10; exit}
      /Wear_Leveling_Count/ {print $10; exit}
      /Percent_Lifetime_Remain/ {print $10; exit}
      /SSD_Life_Left/ {print $10; exit}
    ')"
    echo "${WEAR_RAW:-0}"
    ;;

  status)
    [ -n "$BAY" ] || die "ID sem mapeamento de baia para status"
    STATUS="$(sudo "$SSACLI" ctrl slot="$CTRL_SLOT" pd "$BAY" show detail 2>/dev/null | awk -F': ' '/Status/ {print $2; exit}')"
    case "$STATUS" in
      OK) echo 0 ;;
      "Predictive Failure") echo 1 ;;
      Failed) echo 2 ;;
      *) echo 3 ;;
    esac
    ;;
esac
