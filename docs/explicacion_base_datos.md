# Explicación de Base de Datos - Proyecto_Finanzas_80

Detalle técnico de la persistencia de datos.

## Persistencia Dual
El sistema utiliza una base de datos SQLite llamada solo para fines de desarrollo local: `finanzas_personales.db`.

1. **SQLite (Local)**:
   - Utilizado para desarrollo rápido y pruebas locales.
   - Archivo: `database/finanzas_personales.db`.
   - Motor: `sqlite3` nativo de Python.

2. **Firebase Data Connect (Nube)**:
   - Preparado para escalabilidad a nivel de producción.
   - Integración mediante el directorio `dataconnect/`.
   - Utiliza esquemas GraphQL para la definición de datos en la nube.

## Estructura de Datos
Consulte el archivo [modelo_relacional.md](../database/modelo_relacional.md) para el detalle de campos y tipos.

## Mantenimiento
Se incluye el script `database_setup.py` (en la raíz original) para la inicialización y limpieza de la base de datos local.
