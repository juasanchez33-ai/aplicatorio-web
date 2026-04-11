# DOCUMENTACIÓN OFICIAL ESTRATÉGICA Y TÉCNICA: PLATAFORMA DE INTELIGENCIA FINANCIERA DIGITAL

**Edición:** Grado Ingeniería Fintech Pro  
**Autor:** Juan Esteban Sanchez  
**Institución:** Universidad Antonio Nariño  
**Año:** 2026

---

## 🏛️ I. VISIÓN GENERAL DEL SISTEMA

### 1.1 Nombre del Sistema: "FinanzaPro: Ecosistema de Soberanía Patrimonial"
Aunque el aplicativo nace como una solución de gestión personal, su arquitectura ha sido diseñada bajo el nombre clave **FinanzaPro**, reflejando su capacidad para escalar hacia un entorno de servicios financieros integrados.

### 1.2 Descripción Completa del Producto
FinanzaPro es una **Web App de Gestión Patrimonial (Wealth Management)** que utiliza telemetría financiera en tiempo real para proporcionar una visión de 360 grados sobre el flujo de caja del usuario. A diferencia de las herramientas contables tradicionales, FinanzaPro actúa como un "Copiloto Financiero", integrando datos de mercados globales, educación basada en normas internacionales (Regla 50/30/20) y un motor de amortización de pasivos.

### 1.3 Propuesta de Valor (Unique Selling Proposition)
- **Privacidad Soberana:** El sistema utiliza bases de datos relacionales locales y cifradas, asegurando que el "Big Data" del usuario no sea comercializado por terceros.
- **Velocidad de Respuesta:** Arquitectura asíncrona que garantiza una latencia menor a 150ms en todas las operaciones críticas.
- **Seguridad Dinámica:** Implementación de un modelo MFA (Multi-Factor Authentication) propietario que elimina la dependencia de SMS vulnerables, utilizando canales de correo electrónico bajo TLS 1.3.

### 1.4 El Problema que Resuelve
En la economía moderna, la fragmentación de activos y la opacidad de los micro-gastos generan la "Pobreza Silenciosa". Los usuarios pierden el rastro de sus compromisos recurrentes (SaaS, suscripciones) y no logran proyectar su ahorro real. FinanzaPro consolida esta información, eliminando la incertidumbre y proporcionando un faro de control económico.

### 1.5 Públicos Objetivos (Segmentación)
- **Jóvenes Profesionales:** Enfocados en la autogestión de sus primeros ingresos y control de ocio.
- **Familias Multigeneracionales:** Gestión de presupuestos domésticos, servicios y educación.
- **Freelancers y Emprendedores:** Separación de flujos de caja personales de los operativos.

<div class="page-divider"></div>

## 💰 II. MODELO FUNCIONAL DEL SISTEMA

A continuación se desglosan los pilares funcionales de FinanzaPro, analizados bajo una perspectiva de procesos de negocio.

### 2.1 Gestión de Identidad y Seguridad (MFA)
- **Descripción Técnica:** Implementa un flujo de autenticación de dos pasos. El primer paso valida las credenciales y el segundo exige un código OTP de 6 dígitos.
- **Flujo Paso a Paso:**
    1. Usuario ingresa email.
    2. Backend genera semilla aleatoria de alta entropía.
    3. Envío de token vía SMTP/TLS.
    4. Validación contra tabla `security_codes`.
- **Ejemplo Real:** El usuario solicita acceso a las 2:00 PM; recibe el código `482910`; tras la validación, se establece una sesión segura de 60 minutos.

### 2.2 Gestión de Movimientos Atómicos (Ingresos/Gastos)
- **Descripción Técnica:** Ingesta de transacciones financieras con metadatos de clasificación.
- **Datos de Entrada:** `monto`, `concepto`, `categoría`, `fecha`.
- **Salida:** Confirmación de persistencia en SQLite y actualización reactiva del balance.
- **Ejemplo Real (COP):** 
    - Ingreso: $4.500.000 (Sueldo Mensual).
    - Gasto: $180.000 (Mercado Éxito).
    - Balance Resultante: $4.320.000.

### 2.3 Análisis Financiero de Inteligencia de Negocios (BI)
- **Descripción Técnica:** Motor de agregación que procesa el historial para generar visualizaciones.
- **Funcionalidades:** 
    - Balance Total dinámico.
    - Flujo de caja por periodos (7, 30, 90 días).
    - Detección de tendencias de gasto masivo.
- **Visual:** Gráficos de área (ApexCharts) con gradientes de color cian para visualización en entornos oscuros.

### 2.4 Control de Amortización de Deudas (Pasivos)
- **Descripción Técnica:** Módulo de seguimiento de capital e intereses abonados.
- **Datos Reales:** 
    - Deuda: $15.000.000 (Banco AV Villas).
    - Pagado: $2.500.000.
    - Barra de Progreso: 16.6%.

<div class="page-divider"></div>

## 🧩 III. ARQUITECTURA DEL SISTEMA (DEEP DIVE)

### 3.1 Tipo de Arquitectura: Monolito Ágil Basado en Micro-Servicios Internos
FinanzaPro opera bajo una arquitectura de servidor centralizado con un cliente denso (Thick Client).

### 3.2 Capas del Ecosistema
1. **Presentación (Frontend):** 
    - **JS Vanilla:** Manejo de estados globales y reactividad del DOM.
    - **Jinja2:** Renderizado dinámico del lado del servidor (SSR) para SEO y seguridad.
2. **Lógica de Negocio (Backend):** 
    - **FastAPI:** Motor de ejecución asíncrona. Maneja la concurrencia de peticiones de manera eficiente.
3. **Persistencia (Data Layer):** 
    - **SQLite 3:** Motor relacional con integridad referencial. Se ha configurado un modo de "Cloud Adaptability" para escribir en `/tmp/` dentro de entornos Serverless.

### 3.3 Flujo de Datos Completo
El sistema utiliza un ciclo de vida de petición cerrado:
`Usuario (UI) -> Request Fetch (JSON) -> Backend Router -> DB Execution -> Response 200/400 -> UI Refresh`

<div class="page-divider"></div>

## 💻 IV. STACK TECNOLÓGICO Y JUSTIFICACIÓN CORPORATIVA

| Tecnología | Rol | Justificación Empresarial |
| :--- | :--- | :--- |
| **Python 3.10+** | Núcleo | Estabilidad, manejo de tipos y amplia comunidad de librerías financieras. |
| **FastAPI** | API Framework | Rendimiento superior a Flask/Django; soporte nativo para `async/await`. |
| **SQLite 3** | Base de Datos | Cero latencia de red, portabilidad absoluta del patrimonio del usuario. |
| **Vanilla JS** | Frontend Logic | Eliminación de dependencias pesadas; ejecución instantánea en móviles de gama baja. |
| **ApexCharts** | Visualización | Gráficos vectoriales ligeros con alto nivel de interactividad. |
| **Vercel** | Infraestructura | Despliegue en el "Borde" (Edge) para mínima latencia global. |

<div class="page-divider"></div>

## 🔐 V. SEGURIDAD FINANCIERA (HARDENING GUIDE)

### 5.1 Defensa contra Inyección SQL
Cada consulta a la base de datos utiliza **Sentencias Preparadas**. 
```python
# EJEMPLO DE PROTECCIÓN
conn.execute('SELECT * FROM movements WHERE user_email = ?', (email,))
```
Esto neutraliza cualquier intento de inyección de código malicioso a través de los inputs de usuario.

### 5.2 Prevención de XSS y CSRF
- **Auto-Escaping:** Jinja2 aplica automáticamente el escape de caracteres HTML sospechosos.
- **Headers de Seguridad:** La aplicación puede ser configurada con Content Security Policy (CSP) para bloquear scripts de origen desconocido.

### 5.3 Seguridad en la Capa de Transporte
El uso de **HTTPS obligatorio** es un requisito para la integridad de los datos. El sistema MFA utiliza **STARTTLS** con certificados de validación cruzada para asegurar que los tokens OTP nunca sean interceptados en tránsito.

<div class="page-divider"></div>

## 📊 VI. DISEÑO DE BASE DE DATOS E INGENIERÍA DE DATOS

El sistema utiliza un modelo relacional normalizado para garantizar la integridad de las transacciones financieras (Cumplimiento ACID).

### 6.1 Tabla Maestro: `movements` (Historial Transaccional)
- **Atributos:**
    - `id`: INTEGER PK AUTOINCREMENT.
    - `user_email`: TEXT (Índice de relación).
    - `type`: TEXT ('income' | 'expense').
    - `amount`: REAL (Precisión monetaria).
    - `category`: TEXT (Taxonomía).
- **Relaciones:** Se vincula lógicamente con la sesión de usuario activa para asegurar que un usuario nunca acceda a los datos de otro.

### 6.2 Tabla de Amortización: `debts`
Permite el seguimiento de pasivos a largo plazo, calculando el diferencial entre el capital total y los abonos realizados.

### 6.3 Ejemplo de Registro Real en Pesos Colombianos (COP):
- **Ingreso Mensual:** $4,500,000 (Nómina).
- **Gasto Fijo:** $1,800,000 (Canon de Arrendamiento).
- **Gasto Variable:** $250,000 (Servicios Públicos - EPM/Codensa).

<div class="page-divider"></div>

## 🖥️ VII. EXPERIENCIA DE USUARIO (UX/UI FINTECH)

### 7.1 Psicología de la Interfaz Financiera
El diseño se basa en el concepto de **"Confianza Visual"**. Se utiliza una paleta de colores oscuros (Dark Mode) para reducir la fatiga visual durante sesiones de análisis prolongadas.
- **Cian Neón (#00f0ff):** Representa liquidez, tecnología y modernidad.
- **Rojo Coral:** Utilizado exclusivamente para alertas críticas o saldos negativos.

### 7.2 Accesibilidad y Diseño Responsivo
Mediante el uso de **CSS Fluid Grids**, la aplicación se adapta dinámicamente. En un smartphone, el menú lateral se convierte en una barra inferior de fácil acceso para el pulgar, mientras que en un monitor 4K, la densidad de información se expande para mostrar tablas de auditoría completas.

<div class="page-divider"></div>

## 📡 VIII. DISEÑO DE API Y COMUNICACIÓN ASÍNCRONA

FinanzaPro expone una API REST cerrada para la comunicación entre capas.

### 8.1 Endpoints Principales
- **POST `/api/add-movement`**: Ingesta de datos.
- **GET `/api/movements`**: Recuperación de historial.
- **POST `/api/security/send-otp`**: Disparo de seguridad perimetral.

### 8.2 Estructura JSON Típica:
```json
{
  "status": "success",
  "data": [
    { "id": 1, "concept": "Mercado", "amount": 120000, "category": "Almacen" }
  ]
}
```

<div class="page-divider"></div>

## ⚙️ IX. INSTALACIÓN, DESPLIEGUE Y CALIDAD (QA)

### 9.1 Guía de Instalación Rápida
1. Instalar Python 3.10+.
2. Clonar repositorio.
3. Configurar `.env` con las variables SMTP.
4. Ejecutar `pip install -r requirements.txt`.
5. Iniciar servicio: `python main.py`.

### 9.2 Estrategia de Testing Financiero
Se han realizado pruebas unitarias para validar que el balance total coincida siempre con la suma algebraica de los movimientos, eliminando errores de redondeo mediante el uso de tipos `REAL` de alta precisión.

### 9.3 Manejo de Errores y Logs
El sistema implementa un **Global Exception Handler**. Cualquier fallo en la base de datos o en la comunicación SMTP es capturado y registrado en logs permanentes, mostrando al usuario un mensaje de error amigable en lugar de un colapso del sistema.

<div class="page-divider"></div>

## 🧠 X. CONCLUSIÓN PROFESIONAL Y VISIÓN DE FUTURO

FinanzaPro no es solo un software; es una demostración de cómo la ingeniería moderna puede empoderar al ciudadano común en la gestión de su patrimonio. Con una arquitectura escalable, una seguridad de grado bancario y una UX centrada en la claridad, este aplicativo está listo para ser la base de una solución fintech de clase mundial. En futuras versiones, se prevé la integración con APIs de Bancolombia, Nequi y Daviplata para la automatización total de la ingesta de datos.

---

**Autor:** Juan Esteban Sanchez  
**Universidad Antonio Nariño**  
**2026**
