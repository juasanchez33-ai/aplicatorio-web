# Aplicativo Web de Finanzas Premium



Este es un sistema de gestión financiera moderno, diseñado con una estética de alta fidelidad, efectos de glassmorphism y notificaciones de seguridad integradas.

## ✨ Características Principales
- **Dashboard Dinámico**: Visualización de ingresos, egresos y balance con gráficos interactivos.
- **Seguridad Avanzada**: Sistema de autenticación con MFA (Multi-Factor Authentication) vía SMTP.
- **Interfaz Premium**: Diseño basado en CSS moderno, animaciones fluidas y modo oscuro nativo.
- **Despliegue Continuo**: Configurado para funcionar en plataformas cloud como Koyeb o Railway.

## 🚀 Despliegue en Producción (Koyeb)
El proyecto está optimizado para funcionar en **Koyeb.com**. Sigue estos pasos:
1. Crea una cuenta en [Koyeb](https://app.koyeb.com/) usando tu GitHub.
2. Dale a **"Create Service"** y selecciona **"GitHub"**.
3. Elige el repositorio `aplicatorio-web`.
4. En la configuración:
   - **Type**: Web Service.
   - **Build Command**: `pip install -r requirements.txt` (Suele detectarlo solo).
   - **Run Command**: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`.
5. Configura las siguientes **Environment Variables**:
   - `SMTP_SERVER`: `smtp.gmail.com`.
   - `SMTP_PORT`: `587`.
   - `SMTP_USER`: `juasanchez33@uan.edu.co`.
   - `SMTP_PASS`: `fgqeaetgsuddnrdy`.
   - `DEBUG_SHOW_OTP_IN_CONSOLE`: `False`.
6. ¡Listo! Tu aplicación estará disponible 24/7.

## 🛠️ Desarrollo Local
Si deseas ejecutarlo en tu máquina:
1. Ejecuta `iniciar.bat`.
2. El script configurará automáticamente el entorno virtual (`venv`), las dependencias y la base de datos.
3. El sistema se abrirá en tu navegador en `http://127.0.0.1:8000`.

---
*Desarrollado con ❤️ para una gestión financiera eficiente.*
