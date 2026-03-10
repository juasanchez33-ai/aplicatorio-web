# Instalación del Proyecto - Proyecto_Finanzas_80

Instrucciones para ejecutar el proyecto en un entorno local.

## Requisitos Previos
- Python 3.9 o superior.
- Navegador web moderno (Chrome, Edge, Firefox).

## Pasos de Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd Proyecto_Finanzas_80
   ```

2. **Crear Entorno Virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instalar Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno**:
   - Copie `.env.example` a `.env` y complete sus datos.

5. **Ejecutar el Servidor**:
   ```bash
   cd backend
   python app.py
   ```

El sistema estará disponible en `http://localhost:8000`.
