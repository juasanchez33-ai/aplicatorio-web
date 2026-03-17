# Arquitectura del Sistema - Proyecto_Finanzas_80

Este documento describe la arquitectura técnica del proyecto.

## Stack Tecnológico
- **Backend**: FastAPI (Python 3.x).
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla).
- **Base de Datos**: SQLite (Local) con intención de integración Firebase.
- **Gráficos**: ApexCharts.
- **Estilos**: Tailwind CSS (via CDN) y CSS Custom Properties.

## Capas del Sistema

1. **Capa de Presentación (Frontend)**:
   - Se encarga de la interfaz de usuario.
   - Utiliza una arquitectura de componentes basada en templates de FastAPI.
   - Gestiona la visualización de datos financieros y la interacción a través de un panel lateral (sidebar) y un botón de acción flotante (FAB).

2. **Capa de Lógica (Backend)**:
   - Organizada en rutas modulares (`routes/`).
   - `app.py` actúa como el orquestador principal.
   - Implementa endpoints RESTful para la gestión de usuarios, movimientos, inversiones y deudas.

3. **Capa de Datos**:
   - Persistencia local mediante SQLite.
   - Preparación para escalabilidad con Firebase Data Connect.

## Flujo de Información
El usuario interactúa con el frontend, el cual realiza peticiones `fetch` a los endpoints de FastAPI. El backend procesa las solicitudes, interactúa con la base de datos y retorna respuestas en formato JSON para que el frontend actualice la vista dinámicamente.
