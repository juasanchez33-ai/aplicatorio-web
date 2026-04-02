from fpdf import FPDF
import os
from datetime import datetime

class professionalOfficialManual(FPDF):
    def __init__(self, title_main, author, manual_name, university, year):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(20, 25, 20)
        self.set_auto_page_break(auto=True, margin=30)
        self.title_main = title_main
        self.author = author
        self.manual_name = manual_name
        self.university = university
        self.year = year
        self.set_font('helvetica', '', 14)

    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 11)
            self.set_text_color(120, 120, 120)
            self.cell(0, 10, self.title_main, align='L')
            self.set_x(-30)
            self.cell(0, 10, f'Pág {self.page_no()}', align='R')
            self.line(20, 20, 190, 20)
            self.ln(12)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-25)
            self.set_font('helvetica', 'I', 11)
            self.set_text_color(120, 120, 120)
            self.cell(0, 10, f'{self.author} - {self.manual_name} - {self.year}', align='C')

    def cover(self):
        self.add_page()
        self.set_y(50)
        self.set_font('helvetica', 'B', 32)
        self.set_text_color(0, 70, 140)
        self.multi_cell(0, 15, self.title_main.upper(), align='C')
        
        self.ln(25)
        self.set_font('helvetica', 'B', 22)
        self.set_text_color(80, 80, 80)
        self.cell(0, 15, self.manual_name, align='C', ln=True)
        
        self.set_y(150)
        self.set_font('helvetica', 'B', 20)
        self.set_text_color(0, 0, 0)
        self.cell(0, 12, self.author, align='C', ln=True)
        
        self.set_y(230)
        self.set_font('helvetica', 'B', 18)
        self.multi_cell(0, 10, f'{self.university}\nFacultad de Ingeniería\nBogotá D.C, Colombia\n{self.year}', align='C')

    def table_of_contents(self, chapters_list):
        self.add_page()
        self.set_font('helvetica', 'B', 24)
        self.set_text_color(0, 70, 140)
        self.cell(0, 20, 'ÍNDICE DE CONTENIDO', ln=True)
        self.ln(10)
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(30, 30, 30)
        for i, title in enumerate(chapters_list):
            self.cell(15, 10, f"{i+1}.", align='L')
            self.cell(0, 10, title, align='L', ln=True)
            self.line(20, self.get_y(), 190, self.get_y())
        self.ln(10)

    def chapter(self, num, title, description, img_p=None, img_c=None, code=None):
        self.add_page()
        self.set_font('helvetica', 'B', 22)
        self.set_text_color(0, 70, 140)
        self.multi_cell(0, 15, f'{num}. {title}', align='L')
        self.line(20, self.get_y(), 110, self.get_y())
        self.ln(12)
        
        self.set_font('helvetica', '', 14)
        self.set_text_color(40, 40, 40)
        if isinstance(description, list):
            for p in description:
                self.multi_cell(0, 10, p, align='J')
                self.ln(6)
        else:
            self.multi_cell(0, 10, description, align='J')
            self.ln(6)

        if img_p and os.path.exists(img_p):
            if self.get_y() > 160: self.add_page()
            self.ln(5)
            self.image(img_p, x=25, w=160)
            self.set_font('helvetica', 'I', 11)
            self.cell(0, 12, f'Captura {num}: {img_c or title}', align='C', ln=True)
            self.ln(10)

        if code:
            self.ln(5)
            self.set_font('Courier', 'B', 12)
            self.set_fill_color(248, 248, 248)
            self.multi_cell(0, 8, code, fill=True, border=1)
            self.ln(10)
            self.set_font('helvetica', '', 14)

def run():
    main_title = "Aplicativo Web para el Apoyo de Finanzas Personales"
    author_name = "Juan Esteban Sanchez"
    univ_name = "UNIVERSIDAD ANTONIO NARIÑO"
    year_now = "2026"
    img_root = r"c:\Users\PC\Documents\pagina web de finanzas\aplicativo web\extracted_mockups"
    
    # MANUAL TECNICO Chapters
    tech_data = [
        ("Introducción al Proyecto Financiero 2026", [
            "El presente documento técnico expone la arquitectura y el desarrollo del 'Aplicativo Web para el Apoyo de Finanzas Personales'. Este sistema ha sido concebido para optimizar la gestión contable individual mediante tecnologías web de vanguardia en el año 2026.",
            "El objetivo primordial es proporcionar una plataforma donde el usuario pueda centralizar ingresos, egresos y deudas en un entorno de nube seguro (Serverless), eliminando la dependencia de servidores físicos tradicionales y garantizando una escalabilidad ilimitada ante el crecimiento de la base de registros."
        ], os.path.join(img_root, "page_1_img_1.jpeg"), "Portal de Inicio y Puerta de Autenticación"),
        
        ("Arquitectura de Sistemas y Stack Tecnológico", [
            "La plataforma opera bajo el modelo de Single Page Application (SPA), utilizando JavaScript asíncrono para la orquestación de datos. El stack tecnológico incluye Firebase (Firestore y Auth) para la capa de persistencia y Tailwind CSS para la interfaz reactiva.",
            "Esta arquitectura permite una sincronización en tiempo real. Cada vez que se añade un documento a la base de datos, los listeners de Firestore notifican al cliente y actualizan la interfaz visual mediante componentes dinámicos sin necesidad de recargar la página completa."
        ], os.path.join(img_root, "page_5_img_1.jpeg"), "Dashboard de Análisis Financiero Predictivo"),
        
        ("Diseño UX/UI: Estética Glassmorphism Neon", [
            "La identidad visual del aplicativo se basa en el estilo Glassmorphism, que utiliza transparencias y desenfoques Gaussianos para crear capas de información legibles y elegantes. Esto se logra técnicamente mediante la propiedad 'backdrop-filter: blur(20px)' en CSS.",
            "Adicionalmente, se emplean gradientes neon para resaltar los elementos interactivos críticos, asegurando que el usuario identifique rápidamente las acciones de balance y deudas en entornos de poca iluminación (Modo Oscuro nativo)."
        ], os.path.join(img_root, "page_11_img_1.jpeg"), "Visualización de Gráficas de Tendencia de Ahorro"),
        
        ("Implementación de Persistencia NoSQL", [
            "La base de datos Firestore organiza la información en documentos organizados por colecciones de usuarios. A diferencia de SQL, este modelo permite campos dinámicos que se adaptan a las necesidades de cada usuario sin requerir cambios estructurales costosos.",
            "Se implementaron reglas de validación en el lado del servidor para asegurar que el balance nunca se vea comprometido por peticiones malformadas o ingresos de datos duplicados."
        ], None, None, """// Fragmento de Lógica de Inserción NoSQL
async function addMovement(data) {
    const docRef = await addDoc(collection(db, "movements"), {
        ...data,
        timestamp: serverTimestamp(),
        user: auth.currentUser.email
    });
    return docRef.id;
}"""),
        
        ("Gestión de Deudas y Algoritmos de Pago", [
            "El módulo de deudas (Figura 8) es uno de los componentes más complejos. Utiliza un algoritmo de amortización simple para restar abonos del saldo total de cada deuda registrada por el usuario.",
            "Técnicamente, se lanza una transacción atómica para asegurar que el pago se registre en la colección de transacciones y, simultáneamente, el balance de la deuda se actualice, evitando estados incoherentes en la base de datos."
        ], os.path.join(img_root, "page_8_img_1.jpeg"), "Motor de Control de Pasivos y Acreedores"),
        
        ("Módulo de Educación y Multimedia Native", [
            "Se implementó un reproductor de video nativo para las clases de finanzas personales. Este sistema evita el uso de iframes externos para mejorar la velocidad de carga y cumplir con las políticas de seguridad de contenido (CSP).",
            "La interactividad se gestiona mediante eventos de JavaScript que pausan el video automáticamente si el usuario cambia de pestaña, garantizando un seguimiento óptimo del contenido educativo."
        ], os.path.join(img_root, "page_14_img_1.jpeg"), "Plataforma de Clases Inmersiva"),
        
        ("Seguridad, Despliegue y Mantenimiento", [
            "El proyecto se encuentra desplegado en infraestructura serverless con certificados SSL de 256 bits. Se implementó un flujo de CI/CD para que cada cambio en el código sea validado automáticamente por suites de pruebas unitarias.",
            "El mantenimiento del año 2026 se centra en la actualización de las dependencias del SDK de Firebase para asegurar la compatibilidad con los nuevos navegadores móviles y de escritorio."
        ], os.path.join(img_root, "page_16_img_1.jpeg"), "Configuración de Seguridad y Perfil")
    ]

    # MANUAL USUARIO Chapters
    user_data = [
        ("Bienvenida al Aplicativo Financiero 2026", [
            "¡Enhorabuena por tomar las riendas de su dinero! Este aplicativo ha sido diseñado específicamente para ayudarle a ahorrar, invertir y controlar sus gastos de una manera sencilla y visual.",
            "En esta guía aprenderá a navegar por las diferentes herramientas que hemos preparado para usted en este año 2026. Recuerde que su información está protegida bajo estándares de seguridad internacional."
        ], os.path.join(img_root, "page_1_img_1.jpeg"), "Pantalla de Bienvenida"),
        
        ("Primeros Pasos: Acceso y Seguridad", [
            "Para comenzar, utilice el formulario de inicio de sesión con su correo electrónico registrado. Si ha olvidado su clave, no se preocupe, puede solicitar un enlace de restablecimiento seguro que llegará directamente a su bandeja de entrada.",
            "Le recomendamos utilizar una contraseña robusta que incluya números y símbolos para maximizar la seguridad de su cuenta."
        ], os.path.join(img_root, "page_4_img_1.jpeg"), "Interfaz de Recuperación de Acceso"),
        
        ("Interpretación del Dashboard Principal", [
            "El Dashboard es su centro de comando. En la parte superior verá su saldo disponible total. Las gráficas circulares le mostrarán de un vistazo cuánto dinero está destinando a cada categoría (transporte, alimentación, etc.).",
            "Usted puede filtrar la información por fechas para comparar cómo fue su ahorro en meses anteriores respecto al actual."
        ], os.path.join(img_root, "page_5_img_1.jpeg"), "Vista General de su Estado Financiero"),
        
        ("Gestión de Compras y Movimientos Diarios", [
            "Cada vez que realice una compra, anótela en el botón circular de 'Nueva Transacción'. Puede elegir el icono y el color que prefiera para cada categoría de gasto, haciendo que su historial sea más fácil de entender.",
            "Usted también puede editar o eliminar movimientos antiguos si cometió algún error al escribirlos, manteniendo su contabilidad impecable."
        ], os.path.join(img_root, "page_7_img_1.jpeg"), "Registro de Nuevo Movimiento de Dinero"),
        
        ("Control de Deudas y Abonos a Acreedores", [
            "En la sección de Deudas verá un listado de todas sus obligaciones pendientes. El sistema le mostrará el monto total, cuánto ha pagado y el tiempo restante para liquidar su deuda.",
            "Al realizar un abono, el sistema descontará automáticamente el dinero de su balance total, para que usted no tenga que hacer cálculos manuales."
        ], os.path.join(img_root, "page_8_img_1.jpeg"), "Módulo de Administración de Deudas"),
        
        ("Formación y Clases de Educación Financiera", [
            "No solo se trata de anotar gastos, se trata de aprender. Acceda a nuestro catálogo de videoclases donde expertos le enseñarán técnicas de inversión y ahorro para el largo plazo.",
            "Las clases están disponibles en alta definición y con controles sencillos para que aprenda a su propio ritmo."
        ], os.path.join(img_root, "page_14_img_1.jpeg"), "Portal de Videoclases de Finanzas"),
        
        ("Personalización de su Perfil y Ajustes", [
            "Usted puede cambiar su nombre de usuario, subir una foto de perfil y ajustar la moneda en la que desea ver sus saldos (USD, COP, EUR, etc.) desde la pestaña de configuración.",
            "Mantenga sus datos actualizados para recibir alertas financieras personalizadas según su comportamiento de gasto mensual."
        ], os.path.join(img_root, "page_15_img_1.jpeg"), "Gestión de Perfil y Preferencias de Usuario")
    ]

    # Generate PDFs
    def build_pdf(manual_obj, chapters_data):
        manual_obj.cover()
        manual_obj.table_of_contents([c[0] for c in chapters_data])
        for i, (title, desc, img, cap, *extra) in enumerate(chapters_data):
            code_bit = extra[0] if extra else None
            manual_obj.chapter(i+1, title, desc, img, cap, code_bit)

    # Build Technical Manual
    pdf_t = professionalOfficialManual(main_title, author_name, "MANUAL TÉCNICO DE INGENIERÍA", univ_name, year_now)
    build_pdf(pdf_t, tech_data)
    pdf_t.output("Manual_Técnico.pdf")

    # Build User Manual
    pdf_u = professionalOfficialManual(main_title, author_name, "GUÍA DE USUARIO FINAL", univ_name, year_now)
    build_pdf(pdf_u, user_data)
    pdf_u.output("Manual_Usuario.pdf")

if __name__ == "__main__":
    run()
    print("Manuales Finales Generados (Títulos Únicos + Índice Completo).")
