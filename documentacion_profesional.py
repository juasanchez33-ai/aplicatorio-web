from fpdf import FPDF
import os
from datetime import datetime

class ProfessionalDoc(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(20, 25, 20)
        self.set_auto_page_break(auto=True, margin=25)
        self.custom_accent_color = (0, 160, 255) # Blue
        self.custom_text_color = (40, 40, 40)
        self.custom_title_color = (0, 80, 150)
        self.custom_header_footer_color = (130, 130, 130)

    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(*self.custom_header_footer_color)
            self.cell(0, 10, 'Aplicativo Web para el Manejo de Finanzas Personales - Documentación Oficial', align='L')
            self.set_x(-30)
            self.cell(0, 10, f'Página {self.page_no()}', align='R')
            self.set_draw_color(*self.custom_accent_color)
            self.line(20, 20, 190, 20)
            self.ln(10)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-20)
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(*self.custom_header_footer_color)
            self.cell(0, 10, 'Confidencial - Propiedad Profesional - 2026', align='C')

    def add_page_title(self, title):
        self.set_font('helvetica', 'B', 24)
        self.set_text_color(*self.custom_title_color)
        self.cell(0, 20, title, align='L', new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.custom_accent_color)
        self.line(self.get_x(), self.get_y(), self.get_x() + 170, self.get_y())
        self.ln(10)

    def section_title(self, title):
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(*self.custom_title_color)
        self.cell(0, 12, title, align='L', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def body_text(self, text):
        self.set_font('helvetica', '', 11)
        self.set_text_color(*self.custom_text_color)
        # Handle accents and special characters
        try:
            safe_text = text.encode('latin-1', 'replace').decode('latin-1')
        except:
            safe_text = text
        self.multi_cell(0, 7, safe_text)
        self.ln(5)

    def add_image_page(self, title, img_path, description=""):
        self.add_page()
        self.add_page_title(title)
        if os.path.exists(img_path):
            # Calculate width and height to fit page
            w = 150
            self.image(img_path, x=30, y=self.get_y() + 10, w=w)
            self.set_y(self.get_y() + 110) # Adjust based on image height
        if description:
            self.body_text(description)

def generate_full_doc():
    pdf = ProfessionalDoc()
    
    # --- PÁGINA 1: PORTADA ---
    pdf.add_page()
    # Gradient overlay emulation
    pdf.set_fill_color(240, 248, 255)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.set_y(60)
    pdf.set_font('helvetica', 'B', 32)
    pdf.set_text_color(0, 100, 200)
    pdf.multi_cell(0, 20, 'APLICATIVO WEB PARA EL MANEJO DE FINANZAS PERSONALES', align='C')
    
    pdf.set_y(110)
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 15, 'DOCUMENTACIÓN OFICIAL', align='C', new_x="LMARGIN", new_y="NEXT")
    
    # Logo Placeholder or actual image
    logo_path = r"c:\Users\PC\Documents\pagina web de finanzas\aplicativo web\extracted_mockups\page_1_img_1.jpeg"
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=75, y=140, w=60)
    
    pdf.set_y(220)
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, 'Desarrollador: Jolman Harley Gamboa Salamanca', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, 'Institución: Universidad de Ingeniería y Finanzas', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f'Fecha: {datetime.now().strftime("%d de %B, %Y")}', align='C', new_x="LMARGIN", new_y="NEXT")

    # --- PÁGINA 2: ÍNDICE ---
    pdf.add_page()
    pdf.add_page_title("Índice de Contenido")
    topics = [
        "Introducción ..................................................................... 3",
        "Justificación .................................................................... 4",
        "Objetivos .......................................................................... 5",
        "Alcance del Sistema ........................................................ 6",
        "Descripción General del Sistema ..................................... 7",
        "Flujo General del Usuario ................................................ 8",
        "Arquitectura del Sistema - Frontend ............................... 9",
        "Arquitectura del Sistema - Backend .............................. 10",
        "Tecnologías Utilizadas ................................................... 11",
        "Módulo de Autenticación ............................................... 12",
        "Módulo de Dashboard .................................................... 13",
        "Módulo de Movimientos ................................................ 14",
        "Módulo de Categorías .................................................... 15",
        "Módulo de Deudas .......................................................... 16",
        "Módulo de Pagos ............................................................ 17",
        "Módulo de Educación Financiera .................................. 18",
        "Base de Datos - Estructura General .............................. 19",
        "Base de Datos - Entidades ............................................. 20",
        "Base de Datos - Relaciones ............................................ 21",
        "Base de Datos - Integridad ............................................ 22",
        "Diagrama Entidad-Relación .......................................... 23",
        "Modelo Relacional - Tablas I .......................................... 24",
        "Modelo Relacional - Tablas II ......................................... 25",
        "Funcionamiento del Sistema - Registro ........................ 26",
        "Funcionamiento del Sistema - Gestión ......................... 27",
        "Seguridad del Sistema ................................................... 28",
        "Despliegue y Alojamiento ............................................. 29",
        "Conclusiones .................................................................. 30",
        "Recomendaciones .......................................................... 31",
        "Anexos ............................................................................. 32"
    ]
    pdf.set_font('helvetica', '', 12)
    for topic in topics:
        pdf.cell(0, 8, topic, new_x="LMARGIN", new_y="NEXT")

    # --- PÁGINA 3: INTRODUCCIÓN ---
    pdf.add_page()
    pdf.add_page_title("1. Introducción")
    pdf.body_text("En la era digital actual, la gestión eficiente de las finanzas personales se ha convertido en una necesidad crítica para individuos que buscan alcanzar estabilidad financiera y crecimiento patrimonial. El presente documento detalla el desarrollo y especificaciones técnicas del 'Aplicativo Web para el Manejo de Finanzas Personales', una herramienta integral diseñada para simplificar el seguimiento de ingresos, egresos y deudas.")
    pdf.body_text("Este sistema no solo funciona como una hoja de cálculo avanzada, sino como un ecosistema financiero personal que integra análisis visual, educación financiera y seguridad de grado empresarial. La aplicación ha sido concebida bajo principios de usabilidad y rendimiento, buscando que el usuario final tenga una curva de aprendizaje mínima pero un control máximo sobre su capital.")
    pdf.body_text("A lo largo de esta documentación, se explorarán los fundamentos arquitectónicos, las decisiones tecnológicas y los flujos de trabajo que hacen de este aplicativo una solución robusta y escalable para las finanzas modernas.")

    # --- PÁGINA 4: JUSTIFICACIÓN ---
    pdf.add_page()
    pdf.add_page_title("2. Justificación")
    pdf.body_text("El desarrollo de este sistema surge de la creciente complejidad en la administración de múltiples fuentes de ingresos y diversificación de gastos. Muchas personas carecen de una herramienta centralizada que les permita visualizar su salud financiera de manera clara y rápida.")
    pdf.body_text("La importancia del proyecto radica en tres pilares fundamentales:")
    pdf.section_title("Control Directo")
    pdf.body_text("Permite al usuario identificar fugas de capital y optimizar sus hábitos de consumo mediante el registro meticuloso de cada movimiento financiero.")
    pdf.section_title("Seguridad de la Información")
    pdf.body_text("A diferencia de las libretas físicas o archivos locales sin protección, este sistema utiliza protocolos de autenticación modernos y segundo factor (MFA) para garantizar que los datos financieros sensibles permanezcan privados.")
    pdf.section_title("Educación y Conciencia")
    pdf.body_text("Integra un módulo educativo que fomenta la cultura del ahorro y la inversión, transformando una simple herramienta de registro en un mentor financiero personal.")

    # --- PÁGINA 5: OBJETIVOS ---
    pdf.add_page()
    pdf.add_page_title("3. Objetivos")
    pdf.section_title("Objetivo General")
    pdf.body_text("Desarrollar una plataforma web profesional que permita la gestión integral de las finanzas personales, proporcionando herramientas de visualización de datos, control de deudas y educación financiera bajo un entorno seguro y altamente intuitivo.")
    pdf.section_title("Objetivos Específicos")
    objectives = [
        "Implementar un sistema de autenticación robusto con verificación por SMS para proteger los datos financieros del usuario.",
        "Diseñar una interfaz de usuario moderna basada en Glassmorphism que facilite la interpretación de datos complejos.",
        "Desarrollar un motor de backend asíncrono para garantizar tiempos de respuesta rápidos en la gestión de transacciones.",
        "Integrar librerías de visualización gráfica para representar el comportamiento financiero a través de dashboards dinámicos.",
        "Crear un módulo de persistencia de datos relacional para asegurar la integridad y trazabilidad de los movimientos financieros."
    ]
    for obj in objectives:
        pdf.set_font('helvetica', 'B', 12)
        pdf.write(7, "- ")
        pdf.set_font('helvetica', '', 11)
        pdf.multi_cell(0, 7, obj)
        pdf.ln(3)

    # --- PÁGINA 6: ALCANCE DEL SISTEMA ---
    pdf.add_page()
    pdf.add_page_title("4. Alcance del Sistema")
    pdf.body_text("El alcance de este proyecto abarca todas las fases del ciclo de vida del desarrollo de software, desde la concepción del diseño hasta el despliegue funcional en un entorno web.")
    pdf.section_title("Inclusiones del Sistema")
    pdf.body_text("- Gestión completa de movimientos (Ingresos y Gastos).\n- Panel de control con gráficos estadísticos en tiempo real.\n- Administración de deudas y programación de pagos futuros.\n- Sistema de seguridad MFA (Multi-Factor Authentication).\n- Módulo de personalización de perfil y configuración de visualización.\n- Repositorio de educación financiera interactiva.")
    pdf.section_title("Límites del Proyecto")
    pdf.body_text("- El sistema no se sincroniza directamente con cuentas bancarias externas (API bancaria).\n- No incluye asesoría financiera personalizada mediante Inteligencia Artificial en su versión actual.\n- La aplicación está diseñada principalmente para navegadores web modernos, no cuenta con una aplicación nativa para iOS/Android (aunque es responsiva).")

    # --- PÁGINAS 7-8: DESCRIPCIÓN GENERAL ---
    pdf.add_page()
    pdf.add_page_title("5. Descripción General")
    pdf.body_text("El aplicativo se define como una Single Page Application (SPA) en su comportamiento de usuario, aunque utiliza un backend dinámico para el procesamiento de reglas de negocio. El funcionamiento global se centra en la centralización de datos.")
    pdf.body_text("El usuario comienza su experiencia en un Dashboard unificado que muestra su patrimonio neto actual. A partir de allí, puede navegar hacia la sección de movimientos para registrar transacciones o hacia la gestión de deudas para controlar pasivos.")
    
    # Dashboard Image
    img_dashboard = r"c:\Users\PC\Documents\pagina web de finanzas\aplicativo web\app\static\img\Screenshot_20260309-155608.jpg"
    if os.path.exists(img_dashboard):
        pdf.image(img_dashboard, x=40, y=pdf.get_y() + 10, w=130)
        pdf.set_y(pdf.get_y() + 120)
    pdf.body_text("Figura 1: Vista general del Panel de Control (Dashboard)")

    pdf.add_page()
    pdf.section_title("Flujo del Usuario")
    pdf.body_text("1. Inicio de Sesión: El usuario valida sus credenciales y completa el MFA si es necesario.")
    pdf.body_text("2. Visualización: El sistema carga instantáneamente los gráficos de resumen financiero.")
    pdf.body_text("3. Operación: Se registran nuevos ingresos, gastos o se marcan deudas como pagadas.")
    pdf.body_text("4. Consulta: El usuario filtra movimientos por categorías o fechas para realizar análisis internos.")
    pdf.body_text("5. Estudio: Se accede a la guía educativa para mejorar estrategias de ahorro.")

    # --- PÁGINAS 9-10: ARQUITECTURA ---
    pdf.add_page()
    pdf.add_page_title("6. Arquitectura del Sistema")
    pdf.section_title("Frontend: Tecnología y Diseño")
    pdf.body_text("La capa de presentación está construida con HTML5, CSS3 y Vanilla JavaScript. No se utilizaron frameworks pesados como React para mantener la ligereza y el control absoluto sobre el DOM. Se utiliza Tailwind CSS para el diseño atómico y responsivo.")
    pdf.body_text("El patrón visual es 'Glassmorphism', caracterizado por:")
    pdf.body_text("- Background Blur: Efectos de desenfoque en contenedores.\n- Gradientes Nebula: Fondos profundos con colores azul y purpura.\n- Sombras Suaves: Para dar profundidad a los elementos interactivos.")

    pdf.add_page()
    pdf.section_title("Backend y API")
    pdf.body_text("El servidor utiliza FastAPI (Python 3.9+). Se eligió esta infraestructura por su soporte nativo para 'async/await', lo que permite manejar múltiples peticiones concurrentes sin bloquear el hilo de ejecución principal.")
    pdf.section_title("Diagrama de Arquitectura")
    arch_img = r"c:\Users\PC\Documents\pagina web de finanzas\aplicativo web\extracted_diagrams\page_1_img_1.png"
    if os.path.exists(arch_img):
        pdf.image(arch_img, x=30, y=pdf.get_y() + 5, w=150)
        pdf.set_y(pdf.get_y() + 100)
    pdf.body_text("Figura 2: Diagrama de arquitectura de la plataforma")

    # --- PÁGINA 11: TECNOLOGÍAS ---
    pdf.add_page()
    pdf.add_page_title("7. Tecnologías Utilizadas")
    techs = [
        ("HTML5 & CSS3", "Estructura y estilos avanzados con variables de diseño."),
        ("JavaScript (ES6+)", "Lógica dinámica y comunicación asíncrona mediante Fetch API."),
        ("Python (FastAPI)", "Servidor de alto rendimiento para el manejo de rutas y lógica de negocio."),
        ("SQLite", "Motor de base de datos relacional para persistencia local de alta velocidad."),
        ("Firebase Auth", "Servicio gestionado para identidad y autenticación segura con SMS."),
        ("Firebase Data Connect", "Integración híbrida para sincronización de datos en la nube."),
        ("ApexCharts", "Librería de visualización técnica para dashboards financieros.")
    ]
    for name, desc in techs:
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(*pdf.custom_accent_color)
        pdf.cell(0, 10, name, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(*pdf.custom_text_color)
        pdf.multi_cell(0, 7, desc)
        pdf.ln(2)

    # --- PÁGINAS 12-18: MÓDULOS ---
    modules = [
        ("Autenticación", "Gestión de login, registro y recuperación de cuenta con MFA SMS.", "page_1_img_1.jpeg"),
        ("Dashboard", "Resumen gráfico y balanc financiero global en tiempo real.", "page_2_img_1.jpeg"),
        ("Movimientos", "Registro y auditoría de ingresos y egresos detallados.", "page_3_img_1.jpeg"),
        ("Categorías", "Personalización y clasificación inteligente de gastos.", "page_4_img_1.jpeg"),
        ("Deudas", "Seguimiento de obligaciones financieras y estados de cumplimiento.", "page_5_img_1.jpeg"),
        ("Pagos", "Planificación y control de facturas recurrentes.", "page_6_img_1.jpeg"),
        ("Educación Financiera", "Recursos académicos y guías para el ahorro inteligente.", "page_7_img_1.jpeg")
    ]
    for mod_name, mod_desc, mod_img in modules:
        pdf.add_page()
        pdf.add_page_title(f"Módulo: {mod_name}")
        pdf.body_text(mod_desc)
        img_p = os.path.join(r"c:\Users\PC\Documents\pagina web de finanzas\aplicativo web\extracted_mockups", mod_img)
        if os.path.exists(img_p):
            pdf.image(img_p, x=45, y=pdf.get_y() + 10, w=120)
            pdf.set_y(pdf.get_y() + 140)
        pdf.body_text(f"Visualización profesional del módulo de {mod_name}")

    # --- PÁGINAS 19-22: BASE DE DATOS ---
    pdf.add_page()
    pdf.add_page_title("8. Base de Datos")
    pdf.section_title("Estructura de Datos Relacional")
    pdf.body_text("El sistema utiliza SQLite para garantizar que los datos estén disponibles localmente con tiempos de acceso de milisegundos. La estructura está normalizada para evitar redundancias y asegurar la integridad referencial.")
    pdf.body_text("La arquitectura de datos se divide en entidades maestras y transaccionales.")

    pdf.add_page()
    pdf.section_title("Entidades Principales")
    pdf.body_text("- Usuarios: Almacena perfiles básicos y preferencias de visualización.")
    pdf.body_text("- Movimientos: Contiene el detalle de cada operación financiera.")
    pdf.body_text("- Categorías: Define las agrupaciones para análisis estadístico.")
    pdf.body_text("- Deudas: Registra acreedores y saldos pendientes.")

    pdf.add_page()
    pdf.section_title("Relaciones y Cardinalidad")
    pdf.body_text("1. Un usuario tiene muchos movimientos (1:N).")
    pdf.body_text("2. Un movimiento pertenece obligatoriamente a una categoría (N:1).")
    pdf.body_text("3. Una deuda puede generar múltiples registros de pagos parciales (1:N).")

    pdf.add_page()
    pdf.section_title("Optimización de Consultas")
    pdf.body_text("Para asegurar el rendimiento, se han implementado índices en campos de fecha y categorías, permitiendo que la generación de gráficos en el dashboard sea instantánea incluso con miles de registros históricos.")

    # --- PÁGINA 23: DIAGRAMA ER ---
    pdf.add_page()
    pdf.add_page_title("9. Diagrama Entidad-Relación")
    er_img = r"c:\Users\PC\Documents\pagina web de finanzas\aplicativo web\extracted_diagrams\page_2_img_1.png"
    if os.path.exists(er_img):
        pdf.image(er_img, x=25, y=pdf.get_y() + 10, w=160)
        pdf.set_y(pdf.get_y() + 150)
    pdf.body_text("Figura 3: Modelo lógico de datos y relaciones del sistema")

    # --- PÁGINAS 24-25: MODELO RELACIONAL ---
    pdf.add_page()
    pdf.add_page_title("10. Modelo Relacional")
    pdf.section_title("Especificación de Tablas")
    pdf.body_text("Tabla: movements\n- id(PK, INT)\n- user_id(FK, STRING)\n- amount(FLOAT)\n- type(ENUM: ingreso, egreso)\n- category_id(FK, INT)\n- date(DATETIME)")
    pdf.body_text("Tabla: categories\n- id(PK, INT)\n- name(STRING)\n- color_code(STRING)")

    pdf.add_page()
    pdf.body_text("Tabla: debts\n- id(PK, INT)\n- creditor_name(STRING)\n- total_amount(FLOAT)\n- pending_balance(FLOAT)\n- due_date(DATE)\n- status(ENUM: pendiente, pagado)")
    pdf.body_text("Continuación del modelo relacional detallado según ingeniería de datos.")

    # --- PÁGINAS 26-27: FUNCIONAMIENTO ---
    pdf.add_page()
    pdf.add_page_title("11. Funcionamiento del Sistema")
    pdf.section_title("Proceso de Registro e Ingreso")
    pdf.body_text("El ingreso al sistema se realiza a través de un portal seguro. Si es la primera vez, el sistema solicita los datos básicos de perfil. Si el MFA está activo, se dispara un token SMS al número registrado.")

    pdf.add_page()
    pdf.section_title("Gestión de Datos y Persistencia")
    pdf.body_text("Cada vez que el usuario ingresa un dato, el frontend realiza una validación de tipos. Si es válido, se envía una petición POST al servidor FastAPI, quien se encarga de realizar el COMMIT en la base de datos relacional y devolver el estado actualizado de los gráficos.")

    # --- PÁGINA 28: SEGURIDAD ---
    pdf.add_page()
    pdf.add_page_title("12. Seguridad del Sistema")
    pdf.body_text("La seguridad se maneja en tres niveles estratégicos:")
    pdf.section_title("Capa de Identidad")
    pdf.body_text("Firebase Authentication maneja los tokens de sesión de manera cifrada, evitando ataques de Session Hijacking.")
    pdf.section_title("MFA - Segundo Factor")
    pdf.body_text("Implementación de validación SMS para transacciones críticas y acceso a la configuración de seguridad.")
    pdf.section_title("Seguridad de Datos")
    pdf.body_text("Validaciones en lado del cliente y servidor para prevenir SQL Injection y XSS.")

    # --- PÁGINA 29: DESPLIEGUE ---
    pdf.add_page()
    pdf.add_page_title("13. Despliegue y Alojamiento")
    pdf.body_text("La aplicación está diseñada para ser agnóstica a la infraestructura. Actualmente, el frontend y la lógica de ruteo están preparados para Vercel, mientras que el backend puede alojarse en servicios como Heroku o AWS Lambda.")
    pdf.body_text("Para entornos locales, se proporciona un script 'iniciar.bat' que automatiza el despliegue del servidor Uvicorn en segundos.")

    # --- PÁGINA 30: CONCLUSIONES ---
    pdf.add_page()
    pdf.add_page_title("14. Conclusiones")
    pdf.body_text("El proyecto ha demostrado con éxito que la integración de tecnologías modernas como FastAPI y Firebase puede resultar en una aplicación de finanzas personales extremadamente eficiente y segura.")
    pdf.body_text("Se cumplieron todos los objetivos planteados inicialmente, logrando una plataforma que no solo guarda datos, sino que proporciona valor analítico al usuario.")
    pdf.body_text("La arquitectura modular permite que el sistema crezca en el futuro sin necesidad de una re-ingeniería completa, cumpliendo con los estándares de calidad académica y profesional solicitados.")

    # --- PÁGINA 31: RECOMENDACIONES ---
    pdf.add_page()
    pdf.add_page_title("15. Recomendaciones")
    pdf.body_text("- Implementar un motor de búsqueda avanzada dentro del historial de movimientos.\n- Sincronizar recordatorios de deudas con calendarios externos (Google Calendar).\n- Integrar una API de tasas de cambio para usuarios que manejan divisas extranjeras.")

    # --- PÁGINAS 32-38: ANEXOS ---
    screenshots = [
        ("Dashboard Móvil", "Screenshot_20260309-155616.jpg"),
        ("Vista de Movimientos", "Screenshot_20260309-155621.jpg"),
        ("Gestión de Categorías", "Screenshot_20260309-155624.jpg"),
        ("Detalle de Deudas", "Screenshot_20260309-155635.jpg"),
        ("Recursos Educativos", "Screenshot_20260309-155640.jpg"),
        ("Configuración", "Screenshot_20260309-155643.jpg"),
        ("Perfil de Usuario", "Screenshot_20260309-155645.jpg")
    ]
    for title, img_name in screenshots:
        pdf.add_page()
        pdf.add_page_title(f"Anexo: {title}")
        img_p = os.path.join(r"c:\Users\PC\Documents\pagina web de finanzas\aplicativo web\app\static\img", img_name)
        if os.path.exists(img_p):
            pdf.image(img_p, x=50, y=pdf.get_y() + 10, w=110)
            pdf.set_y(pdf.get_y() + 160)
        pdf.body_text(f"Captura de pantalla real del sistema: {title}")

    # Guardar PDF final
    output_path = r"c:\Users\PC\Documents\pagina web de finanzas\aplicativo web\Documentacion_Profesional_Finanzas.pdf"
    pdf.output(output_path)
    print(f"Documentación profesional generada con éxito: {output_path}")

if __name__ == "__main__":
    generate_full_doc()
