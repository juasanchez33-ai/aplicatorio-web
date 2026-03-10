@echo off
setlocal enabledelayedexpansion
title APLICATIVO WEB FINANZAS - Launcher
cd /d "%~dp0"

echo ==========================================
echo    APLICATIVO WEB PARA EL MANEJO DE FINANZAS PERSONALES
echo ==========================================
echo.

:: STEP 1: Check Python installation
echo [1/3] Verificando instalacion de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] ERROR: Python no esta instalado en este sistema.
    echo.
    pause
    exit /b 1
)

:: STEP 2: Prepare Environment
echo [2/3] Configurando entorno virtual...

if not exist venv (
    echo [*] Creando entorno virtual nuevo...
    python -m venv venv
)

:: Activate and Install
call venv\Scripts\activate
if !errorlevel! neq 0 (
    echo [!] Error al activar el entorno virtual.
    pause
    exit /b 1
)

echo [*] Verificando dependencias...
pip install -r requirements.txt --quiet
if !errorlevel! neq 0 (
    echo [!] Error al instalar las librerias. Reintentando...
    pip install fastapi uvicorn jinja2 python-multipart python-dotenv aiofiles --quiet
)

:: Launch
echo [3/3] Iniciando servidor...
echo.
echo [+] La aplicacion se abrira en: http://localhost:8000
echo.

cd backend
:: Usamos python directamente del venv para evitar ambiguedades
..\venv\Scripts\python.exe app.py

if %errorlevel% neq 0 (
    echo.
    echo [!] El servidor se detuvo. Verifique si el puerto 8000 esta libre.
    pause
)

pause
