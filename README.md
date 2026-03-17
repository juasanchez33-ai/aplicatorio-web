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
3. Configura las variables de entorno (`SMTP_USER`, `SMTP_PASS`, etc.) en el panel de Render.
4. ¡Listo! Tu aplicación estará disponible 24/7 en una URL segura HTTPS.

## 🛠️ Desarrollo Local
Si deseas ejecutarlo en tu máquina:
1. Ejecuta `iniciar.bat`.
2. El script configurará automáticamente el entorno virtual (`venv`), las dependencias y la base de datos.
3. El sistema se abrirá en tu navegador en `http://127.0.0.1:8000`.

---
*Desarrollado con ❤️ para una gestión financiera eficiente.*
