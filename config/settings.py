# CONFIGURAÇÕES DO SISTEMA

# ❗ Use o NOME DNS do DC, não IP
AD_SERVER = "WIN-*******.grupoinlog.local"

# ❗ DC sempre separado por vírgula
BASE_DN = "DC=grupoinlog,DC=local"

# OU para onde o usuário vai durante as férias
OU_FERIAS = "OU=Funcionarios em Ferias,OU=Usuarios,DC=grupoinlog,DC=local"

# CSV (UNC - SEM ACENTO)
CSV_PATH = r"\\WIN-******\Automacao\data\ferias.csv"


# ===== Microsoft 365 =====
TENANT_ID = "4349ca3c-1e1f-4b00-87fb-f181a6e93e28"
CLIENT_ID = "6bc6fd9f-bc3b-4566-a21d-049055b7b80f"
CLIENT_SECRET = "Tnj8Q~4T65Nzs**************"