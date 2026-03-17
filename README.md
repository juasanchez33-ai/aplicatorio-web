# Aplicativo Web de Finanzas Premium



Este es un sistema de gestión financiera moderno, diseñado con una estética de alta fidelidad, efectos de glassmorphism y notificaciones de seguridad integradas.

## ✨ Características Principales
- **Dashboard Dinámico**: Visualización de ingresos, egresos y balance con gráficos interactivos.
- **Seguridad Avanzada**: Sistema de autenticación con MFA (Multi-Factor Authentication) vía SMTP.
- **Interfaz Premium**: Diseño basado en CSS moderno, animaciones fluidas y modo oscuro nativo.
- **Despliegue Continuo**: Configurado para funcionar en **Vercel** mediante `vercel.json`.

## 🚀 Despliegue en Producción (Vercel)
El proyecto está optimizado para funcionar en **Vercel.com**. Sigue estos pasos:
1. Crea una cuenta en [Vercel](https://vercel.com/signup) usando tu GitHub.
2. Dale a **"Add New"** > **"Project"**.
3. Importa el repositorio `aplicatorio-web`.
4. En **Environment Variables**, añade:
   - `SMTP_SERVER`: `smtp.gmail.com`
   - `SMTP_PORT`: `587`
   - `SMTP_USER`: `juasanchez33@uan.edu.co`
   - `SMTP_PASS`: `fgqeaetgsuddnrdy`
   - `DEBUG_SHOW_OTP_IN_CONSOLE`: `False`
5. ¡Listo! Vercel te dará un link seguro (HTTPS) automáticamente.

## 🛠️ Desarrollo Local
Si deseas ejecutarlo en tu máquina:
1. Ejecuta `iniciar.bat`.
2. El script configurará automáticamente el entorno virtual (`venv`), las dependencias y la base de datos.
3. El sistema se abrirá en tu navegador en `http://127.0.0.1:8000`.

---
*Desarrollado con ❤️ para una gestión financiera eficiente.*
