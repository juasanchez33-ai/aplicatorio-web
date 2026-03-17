@echo off
setlocal enabledelayedexpansion
title Aplicativo Web para el Manejo de Finanzas Personales 
cd /d "%~dp0"

echo ==========================================
echo    Aplicativo Web para el Manejo de Finanzas Personales
echo ==========================================
echo.

:: STEP 1: Check Python installation
echo [1/3] Verificando instalacion de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] ERROR: Python no esta instalado en este sistema.
    echo [+] Por favor, descarga e instala Python desde: https://www.python.org/downloads/
    echo [+] Asegurate de marcar la casilla "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

:: STEP 2: Prepare Environment
echo [2/3] Configurando entorno virtual...

if exist venv (
    venv\Scripts\python.exe -c "import sys" >nul 2>&1
    if !errorlevel! neq 0 (
        echo [*] Entorno virtual dañado o de otra version de Python. Recreando...
        rmdir /s /q venv
    )
)

if not exist venv (
    echo [*] Creando entorno virtual nuevo... esto tardara solo un momento...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo [!] Error al crear el entorno virtual.
        pause
        exit /b 1
    )
)

:: Provide explicit python path
set "PY=venv\Scripts\python.exe"


echo [*] Asegurando dependencias actualizadas...
"%PY%" -m pip install --upgrade pip --quiet
"%PY%" -m pip install -r requirements.txt --quiet
if !errorlevel! neq 0 (
    echo [!] Error al instalar las librerias necesarias.
    pause
    exit /b 1
)

echo [*] Preparando base de datos...
"%PY%" database_setup.py
if !errorlevel! neq 0 (
    echo [!] Error al preparar la base de datos.
    pause
    exit /b 1
)

echo [*] Exportando base de datos a SQL legible...
"%PY%" export_db_sql.py >nul 2>&1

:: STEP 3: Launch
echo [3/3] Iniciando servidor y abriendo portal...
echo.
echo [+] ENLACE DE PRODUCCION (Para tu cliente):
echo     https://%RENDER_APP_NAME%.onrender.com
echo.
echo [+] Abriendo el sitio en produccion...
start https://%RENDER_APP_NAME%.onrender.com
echo.
echo [+] Tambien iniciando servidor local para respaldo...
echo     Accede a: http://127.0.0.1:8000
echo.
echo Presiona Ctrl+C para detener el servidor local.
echo ------------------------------------------

"%PY%" main.py

if %errorlevel% neq 0 (
    echo.
    echo [!] El servidor se detuvo de forma inesperada.
    pause
)

pause
