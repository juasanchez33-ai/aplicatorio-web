# DOCUMENTACIÓN TÉCNICA OFICIAL: SISTEMA DE APOYO DE FINANZAS PERSONALES

## 1. Visión General del Proyecto
Este ecosistema digital representa una solución de ingeniería de software diseñada para la soberanía financiera. Integra un backend robusto con FastAPI, una persistencia relacional en SQLite y una interfaz de usuario asíncrona basada en Vanilla JavaScript y Firebase.

---

## 2. Estructura de Directorios (Arquitectura de Carpetas)

El proyecto sigue una estructura modular y organizada para separar claramente la lógica de servidor, la presentación y los activos estáticos.

### 2.1. Directorio Raíz (`/`)
Contiene los archivos de configuración global, scripts de arranque y la base de datos principal.
- `main.py`: El núcleo del servidor. Define las rutas de la API, carga las plantillas y gestiona el ciclo de vida de la aplicación.
- `database_setup.py`: Script de ingeniería de datos. Define el esquema SQL y asegura la integridad referencial de las tablas.
- `generate_pdf.py`: Motor de generación de informes técnicos en formato PDF.
- `iniciar.bat`: Interfaz de despliegue automatizada para entornos Windows.
- `financepro.db`: Nodo central de persistencia (Base de Datos SQLite).
- `requirements.txt`: Especificación de dependencias del ecosistema Python.

### 2.2. Carpeta `app/`
Segmento dedicado a la lógica de aplicación y activos del cliente.
- `app/templates/`: Repositorio de vistas dinámicas procesadas por Jinja2.
- `app/static/`: Contiene todo el código que se sirve directamente al navegador (CSS, JS, Imágenes).

### 2.3. Carpeta `app/static/js/`
El "cerebro" del lado del cliente.
- `app.js`: Coordina la interactividad, el estado global de la aplicación y la comunicación con la API REST.
- `firebase-init.js`: Punto de integración con Google Firebase para la identidad y seguridad.

### 2.4. Carpeta `app/static/css/`
- `styles.css`: Define la estética visual, incluyendo tokens de diseño para Glassmorphism y Nebula Gradient.

### 2.5. Carpeta `explicaciones/`
- Repositorio de documentos markdown complementarios que profundizan en aspectos específicos de la base de datos y la funcionalidad.

---

## 3. Desglose Detallado de Archivos Críticos

### 3.1. Backend: `main.py`
Este archivo implementa el servidor web. Sus responsabilidades incluyen:
- **Gestión de Sesiones**: Validación de usuarios antes de servir contenido.
- **Ruteo**: Despacho de páginas HTML (`/dashboard`, `/movements`, etc.).
- **API REST**: Puntos de entrada para crear, leer, actualizar y borrar (CRUD) datos financieros.
- **Concurrencia**: Uso de funciones asíncronas (`async def`) para maximizar el rendimiento.

### 3.2. Persistencia: `database_setup.py`
Define la topología de la base de datos con tablas como:
- `movements`: Registro de transacciones con metadatos de categoría y fecha.
- `debts`: Seguimiento de pasivos y estados de pago.
- `settings`: Almacenamiento de preferencias de usuario a nivel de servidor.

### 3.3. Frontend Engine: `app.js`
Es una implementación de Single Page Application (SPA). Funciones clave:
- `authCallbackQueue`: Asegura la sincronización entre Firebase y la persistencia local.
- `fetchAllData()`: Orquestador de peticiones AJAX para hidratar la interfaz.
- `startMFA()`: Lógica para el segundo factor de autenticación (SMS).

---

## 4. Seguridad y Autenticación
El sistema utiliza una arquitectura de seguridad híbrida:
1. **Identidad**: Gestionada por Firebase Auth (Cifrado SHA-256).
2. **Segundo Factor (MFA)**: Verificación por SMS para operaciones críticas.
3. **Capa Local**: La base de datos SQLite solo es accesible desde la IP local (127.0.0.1), eliminando riesgos de exposición externa.

---

## 5. Diseño y UX
La interfaz está construida sobre el concepto de **Glassmorphism**, utilizando desenfoque de fondo dinámico y gradientes nebulosos para crear una sensación de profundidad y modernidad. Se utiliza **Tailwind CSS** para un control atómico del diseño responsivo.
