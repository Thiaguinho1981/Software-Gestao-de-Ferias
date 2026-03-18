from ldap3 import Server, Connection, ALL, SASL, GSSAPI, MODIFY_REPLACE
import config.settings as cfg


def conectar_ad():
    server = Server(cfg.AD_SERVER, get_info=ALL)
    return Connection(
        server,
        authentication=SASL,
        sasl_mechanism=GSSAPI,
        auto_bind=True
    )


def obter_dn_usuario(sam):
    conn = conectar_ad()
    conn.search(
        cfg.BASE_DN,
        f"(sAMAccountName={sam})",
        attributes=["distinguishedName"]
    )
    if not conn.entries:
        return None
    return conn.entries[0].distinguishedName.value


def usuario_existe(sam):
    return obter_dn_usuario(sam) is not None


def obter_ou_original(sam):
    conn = conectar_ad()
    conn.search(
        cfg.BASE_DN,
        f"(sAMAccountName={sam})",
        attributes=["distinguishedName"]
    )
    if not conn.entries:
        return None

    dn = conn.entries[0].distinguishedName.value
    return ",".join(dn.split(",")[1:])


def bloquear_usuario(sam):
    dn = obter_dn_usuario(sam)
    if not dn:
        raise Exception("Usuário não encontrado no AD")

    conn = conectar_ad()
    conn.modify(
        dn,
        {"userAccountControl": [(MODIFY_REPLACE, [514])]}
    )


def desbloquear_usuario(sam):
    dn = obter_dn_usuario(sam)
    if not dn:
        raise Exception("Usuário não encontrado no AD")

    conn = conectar_ad()
    conn.modify(
        dn,
        {"userAccountControl": [(MODIFY_REPLACE, [512])]}
    )


def mover_para_ferias(sam):
    dn = obter_dn_usuario(sam)
    conn = conectar_ad()
    conn.modify_dn(
        dn,
        f"CN={dn.split(',')[0].replace('CN=', '')}",
        new_superior=cfg.OU_FERIAS
    )


def mover_para_ou_original(sam, ou_original):
    dn = obter_dn_usuario(sam)
    conn = conectar_ad()
    conn.modify_dn(
        dn,
        f"CN={dn.split(',')[0].replace('CN=', '')}",
        new_superior=ou_original
    )