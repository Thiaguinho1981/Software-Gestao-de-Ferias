import tkinter as tk
from tkinter import messagebox
import pandas as pd
from core.m365 import bloquear_usuario_m365
from config.settings import CSV_PATH
from core.ad import (
    usuario_existe,
    obter_ou_original,
    bloquear_usuario,
    mover_para_ferias
)



def cadastrar():
    sam = entry_sam.get()
    email = entry_email.get()
    data = entry_data.get()

    if not sam.strip() or not email.strip():
        messagebox.showwarning("Erro", "Login AD e e-mail são obrigatórios")
        return

    if not usuario_existe(sam):
        messagebox.showerror(
            "Usuário não encontrado",
            "Usuário não encontrado no Active Directory"
        )
        return

    ou_original = obter_ou_original(sam)

    df = pd.read_csv(CSV_PATH)
    df.loc[len(df)] = [sam, email, ou_original, data, False]
    df.to_csv(CSV_PATH, index=False)

    bloquear_usuario(sam)
    mover_para_ferias(sam)
    bloquear_usuario_m365(email)

    messagebox.showinfo(
        "Sucesso",
        "Usuário bloqueado no AD e no Microsoft 365"
    )


def iniciar_interface():
    root = tk.Tk()
    root.title("Gestão de Férias - AD + M365")

    tk.Label(root, text="Login do Usuário (AD)").pack()
    global entry_sam
    entry_sam = tk.Entry(root, width=40)
    entry_sam.pack()

    tk.Label(root, text="Email Microsoft 365").pack()
    global entry_email
    entry_email = tk.Entry(root, width=40)
    entry_email.pack()

    tk.Label(root, text="Data de Retorno (YYYY-MM-DD)").pack()
    global entry_data
    entry_data = tk.Entry(root)
    entry_data.pack()

    tk.Button(
        root,
        text="Cadastrar Férias",
        command=cadastrar
    ).pack(pady=10)

    root.mainloop()