@echo off
title Abrir Interface - Gestao de Ferias

REM === AJUSTE PARA A PASTA DO SEU PROJETO ===
cd /d "C:\Users\thiago.almeida\Desktop\Auto"

REM === ATIVA A VENV ===
call .venv\Scripts\activate.bat

REM === DEBUG (CONFIRMAR CONTEXTO) ===
echo Diretorio atual:
cd
echo Python em uso:
where python

REM === ABRE A INTERFACE ===
python run.py ui

pause