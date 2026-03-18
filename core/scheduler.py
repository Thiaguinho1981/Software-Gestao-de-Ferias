import pandas as pd
from datetime import datetime
from core.ad import desbloquear_usuario, mover_para_ou_original
from core.m365 import desbloquear_usuario_m365
from config.settings import CSV_PATH


def executar_rotina():
    hoje = datetime.now().date()

    df = pd.read_csv(CSV_PATH)

    # 🔧 normaliza reativado para boolean
    df["reativado"] = df["reativado"].astype(str).str.lower() == "true"

    for i, row in df.iterrows():
        if row["reativado"]:
            continue

        data_retorno = datetime.strptime(
            str(row["data_retorno"]).strip(),
            "%Y-%m-%d"
        ).date()

        if hoje >= data_retorno:
            desbloquear_usuario(row["nome"])
            mover_para_ou_original(row["nome"], row["ou_original"])
            desbloquear_usuario_m365(row["email"])
            df.at[i, "reativado"] = True

    # 🔽 salva CSV como texto (true/false)
    df["reativado"] = df["reativado"].astype(str).str.lower()
    df.to_csv(CSV_PATH, index=False)