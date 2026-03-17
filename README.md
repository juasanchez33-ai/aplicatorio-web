# Aplicativo Web de Finanzas Premium

Este es un sistema de gestión financiera moderno, diseñado con una estética de alta fidelidad, efectos de glassmorphism y notificaciones de seguridad integradas.

## ✨ Características Principales
- **Dashboard Dinámico**: Visualización de ingresos, egresos y balance con gráficos interactivos.
- **Seguridad Avanzada**: Sistema de autenticación con MFA (Multi-Factor Authentication) vía SMTP.
- **Interfaz Premium**: Diseño basado en CSS moderno, animaciones fluidas y modo oscuro nativo.
- **Despliegue Continuo**: Configurado para despliegue automático en Render.com mediante `render.yaml`.

## 🚀 Despliegue en Producción
El proyecto está optimizado para funcionar en **Render.com**. Sigue estos pasos:
1. Conecta este repositorio a un nuevo "Web Service" en Render.
2. Render detectará automáticamente el archivo `render.yaml`.
3. Configura las siguientes Variables de Entorno en el panel de Render:
   - `SMTP_SERVER`: Tu servidor de correo (ej. `smtp.gmail.com`).
   - `SMTP_PORT`: Generalmente `587`.
   - `SMTP_USER`: Tu correo electrónico.
   - `SMTP_PASS`: Tu contraseña de aplicación.
   - `RENDER_APP_NAME`: El nombre que le diste a la app en Render.
   - `DEBUG_SHOW_OTP_IN_CONSOLE`: `False` (Recomendado en producción).
4. ¡Listo! Tu aplicación estará disponible 24/7 en una URL segura HTTPS.

## 🛠️ Desarrollo Local
Si deseas ejecutarlo en tu máquina:
1. Ejecuta `iniciar.bat`.
2. El script configurará automáticamente el entorno virtual (`venv`), las dependencias y la base de datos.
3. El sistema se abrirá en tu navegador en `http://127.0.0.1:8000`.

---
*Desarrollado con ❤️ para una gestión financiera eficiente.*
