# MANUAL TÉCNICO - Aplicativo Web para el Manejo de Finanzas Personales

## 1. Introducción
Aplicativo Web para el Manejo de Finanzas Personales es una plataforma web avanzada de gestión de finanzas personales diseñada para ofrecer a los usuarios una visión clara y detallada de su salud financiera. El sistema integra herramientas de seguimiento de movimientos, administración de pagos y recursos educativos.

## 2. Descripción del Sistema
El aplicativo utiliza una arquitectura moderna basada en un frontend dinámico y un backend ligero. La persistencia de datos y la autenticación se manejan a través de Firebase, garantizando seguridad y sincronización en tiempo real.

### Arquitectura de Software
- **Modelo:** SQLite (Base de datos relacional `financepro.db`).
- **Vista:** Plantillas HTML con Tailwind CSS y ApexCharts.
- **Controlador:** Lógica en JavaScript (`app.js`) y API de FastAPI (`main.py`).

## 3. Características Técnicas
- **Autenticación:** Firebase Admin SDK / Client SDK (Google Sign-In e Identity Platform).
- **Base de Datos:** SQLite 3 para persistencia local de movimientos, deudas y pagos.
- **Visualización:** ApexCharts para gráficos financieros dinámicos.
- **Estilo:** Tailwind CSS con diseño Glassmorphism y Nebula Gradient.

## 4. Requisitos de Hardware y Software
### Hardware
- Procesador: Dual Core 2.0GHz o superior.
- Memoria RAM: 4 GB mínimo.
- Almacenamiento: 200 MB de espacio libre.

### Software
- Sistema Operativo: Windows 10, macOS or Linux.
- Python 3.9 o superior.
- Navegador Web moderno (Chrome, Edge, Firefox).

## 5. Instrucciones de Instalación
1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/finance-pro
    cd finance-pro
    ```
2.  **Configurar entorno virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configurar Firebase:**
    - Crear un proyecto en la consola de Firebase.
    - Copiar las credenciales en `app/static/js/firebase-init.js`.
5.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```

## 6. Estructura del Proyecto
- `main.py`: Punto de entrada del servidor FastAPI.
- `app/templates/`: Vistas HTML del sistema.
- `app/static/js/`: Lógica del sistema (Firebase e interacciones).
- `app/static/css/`: Estilos personalizados y tokens de diseño.

## 7. Solución de Problemas
| Problema | Causa Probable | Solución |
| :--- | :--- | :--- |
| Error de Autenticación | Credenciales de Firebase vencidas o incorrectas. | Revisar `firebase-init.js`. |
| Gráficos no cargan | Fallo en la conexión CDN de ApexCharts. | Verificar conexión a internet. |
| Datos no persisten | Error en archivo SQLite o permisos de escritura. | Verificar existencia de `financepro.db` y permisos de carpeta. |

---
**Desarrollado por:** Jolman Harley Gamboa Salamanca  
**Año:** 2026
