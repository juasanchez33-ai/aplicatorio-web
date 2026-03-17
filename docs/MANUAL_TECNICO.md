# MANUAL TÉCNICO - APLICATIVO WEB PARA EL MANEJO DE FINANZAS PERSONALES

## 1. RESUMEN DEL SISTEMA
**Proyecto Finanzas 80** es una aplicación web robusta construida con una arquitectura desacoplada. Utiliza **FastAPI** para el backend y una interfaz rica en **Vanilla JS** y **CSS Custom Properties** para el frontend.

## 2. ARQUITECTURA TÉCNICA
### Backend (Python/FastAPI)
- **Rutas Modulares**: Divididas por dominio (auth, movements, investments).
- **Inyección de Dependencias**: Gestión eficiente de conexiones a la base de datos.
- **Asincronía**: Procesamiento no bloqueante de peticiones.

### Frontend (HTML/JS/CSS)
- **Estructura**: Organización en carpetas `css/`, `js/` y `assets/`.
- **Lógica**: JavaScript modular para interacción con la API y Firebase.
- **Estilos**: Sistema de tokens de diseño para garantizar consistencia visual y soporte de temas.

## 3. MODELO DE DATOS (SQLITE)
El sistema utiliza SQLite como motor de persistencia local.
- **Tablas principales**: `users`, `movements`, `investments`, `debts`, `payments`.
- **Archivo de DB**: `database/finanzas_personales.db`.
- **Diagrama**: Disponible en `database/diagrama_entidad_relacion.png`.

## 4. INTEGRACIÓN CON FIREBASE
El sistema está configurado para utilizar Firebase en:
- **Autenticación**: Gestión de sesiones de usuario.
- **Data Connect**: Sincronización escalable en la nube (directorio `dataconnect/`).

## 5. DESPLIEGUE LOCAL
1. **Script de Inicio**: `iniciar.bat` automatiza la creación del `venv` y la instalación de dependencias.
2. **Servidor**: El backend corre en el puerto 8000 mediante `uvicorn`.
3. **Frontend**: El servidor sirve archivos estáticos desde las carpetas configuradas en `app.py`.

## 6. MANTENIMIENTO Y EXTENSIÓN
- Para añadir una nueva ruta: Cree un archivo en `backend/routes/` e inclúyalo en `app.py`.
- Para cambiar estilos: Modifique `frontend/css/styles.css`.
- Para actualizar la base de datos: Use scripts de migración o `database_setup.py`.

---
*Documentación avanzada para fines de desarrollo.*
