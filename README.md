## Autor

Projeto desenvolvido por **Thiago Henrique**  
Analista de Infraestrutura | Automação | Python
Projeto voltado para automação de gestão de férias com integração AD e Microsoft 365.

# Software de Gestão de Férias

Aplicação desenvolvida em Python para automação do bloqueio e desbloqueio de colaboradores em período de férias, com integração ao **Active Directory (AD)** e ao **Microsoft 365**.

---

## Visão Geral

O sistema foi criado para automatizar o processo de afastamento temporário de usuários que entrarão em férias, realizando:

- bloqueio automático da conta no **Active Directory**
- bloqueio automático da conta no **Microsoft 365**
- desbloqueio automático na data de retorno informada
- execução manual ou automatizada via **Agendador de Tarefas**

Para que a automação ocorra corretamente, é necessário informar:

- **login do usuário**
- **e-mail do colaborador**
- **data de retorno**

A data de retorno deve ser preenchida corretamente para que o desbloqueio automático aconteça no dia previsto.

---

## Objetivo

Padronizar e automatizar a rotina de gestão de férias, reduzindo falhas operacionais, aumentando a segurança de acesso e garantindo que o bloqueio e desbloqueio de contas ocorra de forma controlada e previsível.

---

## Estrutura do Projeto

```bash
software-gestao-ferias/
├── app/
│   └── app.py
├── config/
│   └── settings.py
├── core/
│   ├── ad_manager.py
│   ├── ad.py
│   ├── m365.py
│   └── scheduler.py
├── data/
│   └── ferias.csv
├── abrir_interface.bat
├── run.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Componentes do Projeto

### `app/`
Camada de interface e inicialização da aplicação.

- `app.py`: controle principal da interface e fluxo de execução

### `config/`
Centraliza as configurações do sistema.

- `settings.py`: armazena parâmetros de autenticação e configurações da aplicação

### `core/`
Contém a lógica principal da automação.

- `ad_manager.py`: gerenciamento de operações relacionadas ao AD
- `ad.py`: funções auxiliares e integração com Active Directory
- `m365.py`: integração com Microsoft 365 / Microsoft Graph
- `scheduler.py`: controle de execução automática e rotinas agendadas

### `data/`
Contém os arquivos de dados utilizados pela aplicação.

- `ferias.csv`: base de dados usada no processamento das férias

### Arquivos principais
- `run.py`: ponto de entrada principal do sistema
- `abrir_interface.bat`: facilitador de execução no Windows
- `requirements.txt`: dependências do projeto
- `README.md`: documentação do sistema

---

## Requisitos do Ambiente

Antes de utilizar a aplicação, o ambiente precisa estar corretamente configurado.

### Requisitos básicos

- Python 3
- pip
- Windows
- acesso ao domínio
- conectividade com o Active Directory
- credenciais válidas do Microsoft Entra ID / Azure

---

## Requisito de DNS para Active Directory

Para que a automação funcione corretamente com o **Active Directory**, a máquina que executa o sistema deve estar com o **DNS apontando para o servidor do AD**.

Isso é necessário porque o Active Directory depende do DNS para:

- localizar controladores de domínio
- resolver o nome do servidor
- autenticar usuários no domínio
- permitir consultas LDAP corretamente

### Problemas que podem ocorrer com DNS incorreto

- erro de conexão com o domínio
- falha na movimentação de usuários entre OUs
- impossibilidade de habilitar ou desabilitar contas
- erro de autenticação

> **Importante:** o apontamento correto do DNS é essencial para garantir comunicação estável e segura com o domínio.

---

## Configuração de Integração com Microsoft 365

Para a integração com o Microsoft 365 funcionar corretamente, o sistema utiliza credenciais da aplicação registrada no **Microsoft Entra ID (Azure)**.

As informações necessárias são:

- `TENANT_ID`
- `CLIENT_ID`
- `CLIENT_SECRET`

### O que significa cada credencial

#### `TENANT_ID`
Identifica a organização dentro do Microsoft 365.

#### `CLIENT_ID`
Identifica a aplicação registrada no Azure (App Registration).

#### `CLIENT_SECRET`
Funciona como a senha da aplicação e é utilizado para obter o token de acesso junto ao Microsoft Graph.

Esse token permite executar ações como:

- bloquear contas no Microsoft 365
- desbloquear contas no Microsoft 365

> **Atenção:** o `CLIENT_SECRET` possui validade e deve ser renovado antes do vencimento. Se ele expirar, a automação continuará funcionando no Active Directory, mas deixará de executar alterações no Microsoft 365.

---

## Arquivo de Configuração

As credenciais do Microsoft 365 ficam no arquivo:

```python
config/settings.py
```

Exemplo:

```python
TENANT_ID = "xxxxxxxx"
CLIENT_ID = "xxxxxxxx"
CLIENT_SECRET = "xxxxxxxx"
```

### Regra importante
Quando a chave expirar, **somente o valor de `CLIENT_SECRET` deve ser alterado**.

Não deve ser alterado:

- `TENANT_ID`
- `CLIENT_ID`

---

## Como Solicitar uma Nova Client Secret

### 1. Acessar o Azure

Entrar no portal:

```text
https://portal.azure.com
```

Ir em:

```text
Microsoft Entra ID
```

### 2. Acessar a aplicação

Caminho:

```text
App registrations
→ selecionar a aplicação
```

### 3. Criar uma nova secret

Ir em:

```text
Certificates & secrets
```

Clicar em:

```text
New client secret
```

Preencher, por exemplo:

- **Description:** `Automacao_Ferias_2026_2027`
- **Expiration:** `12 months`

Depois clicar em:

```text
Add
```

### Ponto crítico

Quando a nova secret for criada, o Azure exibirá o campo:

```text
Value
```

Esse valor deve ser **copiado imediatamente**, porque depois que a tela for fechada ele não poderá mais ser visualizado.

---

## Boas Práticas para Renovação da Secret

- criar a nova secret antes da antiga vencer
- atualizar o sistema com a nova chave
- testar o funcionamento
- excluir a antiga somente após validação

---

## Instalação do Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/software-gestao-ferias.git
```

### 2. Entrar na pasta do projeto

```bash
cd software-gestao-ferias
```

### 3. Criar ambiente virtual

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Como Executar

### Execução padrão

```bash
python run.py
```

### Execução pelo arquivo BAT

No Windows, também é possível executar usando:

```text
abrir_interface.bat
```

---

## Geração do Executável

Sempre que houver qualquer alteração no código-fonte — incluindo:

- atualização do `CLIENT_SECRET`
- ajustes de lógica
- correções no sistema

é obrigatório recriar o executável.

### Passo 1 — Acessar a pasta do projeto

Abrir o Prompt de Comando ou PowerShell e navegar até a raiz do projeto:

```bash
cd C:\Caminho\Do\Projeto
```

### Passo 2 — Gerar o executável com PyInstaller

```bash
python -m PyInstaller --onefile --noconsole --name Bloqueio_Ferias run.py
```

### Explicação dos parâmetros

- `--onefile` → gera um único executável
- `--noconsole` → impede a abertura da janela do CMD
- `--name Bloqueio_Ferias` → define o nome do executável
- `run.py` → arquivo principal da aplicação

### Passo 3 — Localizar o executável gerado

Após a geração, o arquivo ficará em:

```bash
dist\Bloqueio_Ferias.exe
```

---

## Publicação em Produção

Após gerar o novo executável:

### Passo 4 — Substituir no servidor

Copiar o executável novo e substituir o antigo no caminho:

```bash
C:\Automacao\dist\
```

### Passo 5 — Testar manualmente no servidor

Antes de depender da execução automática, testar manualmente:

```bash
cd C:\Automacao
.\dist\Bloqueio_Ferias.exe auto
```

Se não houver erro, o sistema estará pronto para uso com o **Agendador de Tarefas**.

---

## Fluxo Operacional do Sistema

De forma geral, o sistema segue este fluxo:

1. recebe os dados do colaborador
2. valida login, e-mail e data de retorno
3. processa a lógica de bloqueio
4. executa ações no Active Directory
5. executa ações no Microsoft 365
6. agenda ou processa o desbloqueio na data prevista
7. pode ser executado manualmente ou de forma automatizada

---

## Arquivo de Dados

O sistema utiliza o arquivo:

```text
data/ferias.csv
```

Esse arquivo pode ser usado como base para:

- lista de colaboradores
- datas de férias
- datas de retorno
- controle operacional da automação

---

## Segurança

Por se tratar de integração com serviços corporativos, recomenda-se:

- restringir acesso ao código-fonte
- proteger o arquivo `settings.py`
- não compartilhar `CLIENT_SECRET`
- manter controle sobre validade das credenciais
- validar a automação sempre após alteração de credenciais
- recriar o executável após qualquer ajuste sensível

---

## Boas Práticas de Versionamento

Versionar no GitHub apenas arquivos essenciais do projeto:

### Versionar
- código-fonte
- arquivos de configuração
- documentação
- dependências

### Não versionar
- executáveis gerados
- arquivos temporários
- cache de Python
- artefatos de build

Exemplo de fluxo:

```bash
git init
git add .
git commit -m "Primeiro commit"
git branch -M main
git remote add origin https://github.com/seu-usuario/software-gestao-ferias.git
git push -u origin main
```

---

## Melhorias Futuras

- adicionar logs estruturados
- validar automaticamente o arquivo CSV
- implementar tratamento de erros mais detalhado
- separar credenciais de configuração em variáveis de ambiente
- adicionar testes automatizados
- melhorar interface de operação e monitoramento

---

## Autor

Projeto voltado para automação corporativa de gestão de férias, com integração a ambientes Microsoft e rotinas administrativas.

---

## Licença

Definir conforme a política de uso da empresa ou do autor do projeto.


## Autor

Projeto desenvolvido por **Thiago Henrique**  
Analista de Infraestrutura | Automação | Python
Projeto voltado para automação de gestão de férias com integração AD e Microsoft 365.