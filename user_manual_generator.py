import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class UserMegaManual(FPDF):
    def __init__(self, main_title, subtitle, author):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(25, 30, 25)
        self.set_auto_page_break(auto=True, margin=35)
        self.main_title = main_title
        self.subtitle = subtitle
        self.author = author

    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'B', 12)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, self.main_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
            self.set_x(-35)
            self.set_y(30)
            self.cell(0, 10, f'Pág. {self.page_no()}', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
            self.line(25, 40, 185, 40)
            self.set_y(45)

    def cover_and_index(self, sections):
        self.add_page()
        self.set_y(40)
        self.set_font('helvetica', 'B', 28)
        self.set_text_color(0, 80, 40) # Greenish for finance vibe
        self.multi_cell(0, 14, self.main_title, align='C')
        
        self.ln(10)
        self.set_font('helvetica', 'I', 20)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 10, self.subtitle, align='C')
        
        self.set_y(130)
        self.set_font('helvetica', 'B', 22)
        self.set_text_color(0, 100, 50)
        self.cell(0, 10, "ÍNDICE DE NAVEGACIÓN Y AYUDA", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.line(25, self.get_y(), 140, self.get_y())
        self.ln(8)
        
        self.set_text_color(40, 40, 40)
        idx = [s["title"] for s in sections if s["type"] == "chapter"]
        for i, title in enumerate(idx):
            if self.get_y() > 260:
                self.add_page()
            y = self.get_y()
            self.set_font('helvetica', 'B', 18)
            self.set_xy(25, y)
            self.cell(15, 12, f"{i+1}.")
            self.set_font('helvetica', '', 18)
            self.set_xy(40, y)
            self.multi_cell(0, 12, title, align='L')

    def chapter_title(self, num, title):
        self.set_font('helvetica', 'B', 26)
        self.set_text_color(0, 100, 50)
        self.multi_cell(0, 14, f'PASO {num}. {title}', align='L')
        self.line(25, self.get_y(), 170, self.get_y())
        self.ln(15)

    def chapter_body(self, text):
        self.set_font('helvetica', '', 16)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 10, text, align='J')
        self.ln(8)

    def tip_box(self, text):
        self.ln(5)
        self.set_fill_color(230, 250, 230)
        self.set_draw_color(100, 200, 100)
        self.set_font('helvetica', 'I', 15)
        self.set_text_color(0, 80, 0)
        self.multi_cell(0, 10, f" >>> CONSEJO ÚTIL: {text}", border=1, fill=True, align='L')
        self.set_draw_color(0, 0, 0)
        self.ln(10)

    def add_image(self, img_path, caption):
        if os.path.exists(img_path):
            if self.get_y() > 160:
                self.add_page()
            self.ln(10)
            self.image(img_path, w=150, x=30)
            self.ln(6)
            self.set_font('helvetica', 'B', 13)
            self.set_text_color(80, 80, 80)
            self.multi_cell(0, 8, caption, align='C')
            self.ln(12)

# --- INICIO SECCIONES ---
sections = [
    {
        "type": "chapter",
        "title": "BIENVENIDA AL APLICATIVO WEB",
        "content": [
            "Bienvenido al Aplicativo Web para el Manejo de Finanzas Personales. Esta guía paso a paso te enseñará detalladamente cómo tomar el control absoluto de tus cuentas, ingresos y egresos de manera visual, rápida y segura en tu navegador.",
            "Para un usuario moderno, organizarse no debería ser un proceso técnico ni requerir contadores avanzados. El sistema está fundamentado en clics intuitivos y menús guiados que reaccionan inmediatamente ante cada acción. Abordaremos cómo arrancar desde cero hasta que domines el tablero y programes pagos automáticamente."
        ]
    },
    {
        "type": "chapter",
        "title": "CREANDO UNA NUEVA CUENTA (REGISTRO)",
        "content": [
            "EXPERIENCIA DE ALTA EXCLUSIVA:\nEl acceso a esta plataforma es privado, por lo que el primer paso en tu experiencia consiste en registrarte con tus datos fidedignos. ",
            "1. Clic en 'Crear Cuenta': En la pantalla principal verás un botón azul brillante. Púlsalo para desplegar la bóveda de registro.\n\n2. Ingreso de Datos: Se te solicitará un número de documento que funciona para validaciones en tu país (Cédula). Escribe tu Nombre Completo y un Correo Electrónico válido y activo.\n\n3. Clave Segura: Genera una contraseña. Asegúrate de incluir números para que el sistema te apruebe el registro y no olvides confirmar la lectura de Términos."
        ],
        "image": "docs/assets/register_module.png",
        "caption": "Figura 1. Ingresando los datos primarios para crear la sesión y perfilar a la persona."
    },
    {
        "type": "tip",
        "content": "Tu correo debe ser real, ya que el sistema lo usará siempre como capa de máxima seguridad antes de permitir el ingreso en áreas confidenciales."
    },
    {
        "type": "chapter",
        "title": "EL ACCESO DE SEGURIDAD EXTREMA",
        "content": [
            "CÓMO INGRESAR DE MANERA CONFIDENCIAL:\nUna vez registrado, vuelve al inicio. Al darle clic en Iniciar Sesión, escribirás únicamente tu correo y tu contraseña. ¡Pero la puerta aún no se abrirá por completo!",
            "El sistema es tan estricto que mandará rápidamente un Número de Código de Validación a la bandeja de entrada de tu correo afiliado. Abre tu aplicación de Google Mail o Outlook, lee los 6 dígitos temporales e insértalos en la plataforma. Este candado (MFA) evita que curiosos revisen tus finanzas."
        ],
        "image": "docs/assets/login_page.png",
        "caption": "Figura 2. Bloque de protección. Ninguna persona entrará sin la llave despachada a tu celular/correo."
    },
    {
        "type": "chapter",
        "title": "CONOCIENDO TU TABLERO DE MANDOS (DASHBOARD)",
        "content": [
            "NAVEGACIÓN CENTRAL:\nTras pasar el cristal de protección, visualizarás el núcleo de la aplicación. Esta experiencia de interfaz gráfica cuenta con un diseño de Modo Oscuro Avanzado. En la primera franja lateral izquierda tienes tu menú principal (Rutas directas a todas las facetas).",
            "El indicador numérico gigante que ves centrado en la pantalla (Ej. $ 5,000.00) es el BALANCE NETO DE CAPITAL, es decir, lo que posees en tu bolsillo o bancos tras restar todas las salidas.",
            "Toda gráfica colorida que visualices allí se moverá e irá trazando tendencias interactivas al momento de ingresar valores."
        ],
        "image": "docs/assets/dashboard_main.png",
        "caption": "Figura 3. Gráficas analíticas e indicadores que reaccionan con un nivel total de usabilidad y comprensión visual."
    },
    {
        "type": "chapter",
        "title": "AÑADIR GASTOS E INGRESOS EN SEGUNDOS",
        "content": [
            "CÓMO EFECTUAR UNA TRANSACCIÓN DIARIA:\nNo es necesario cambiar de hoja ni llenar listas complejas.\n\n1. En la parte central observarás un botón iluminado que dice 'Agegar Movimiento' o un botón rápido circular naranja/verde. Haz clic ahí.\n\n2. Aparecerá inmediatamente una ventana flotante de cristal. Selecciona el Tipo: ¿Es Dinero Entrante (Ingreso) o Dinero Saliente (Gasto)?\n\n3. Anota su Monto (ej: 15.00), e incluye una 'Etiqueta Libre' recordando por qué cediste ese dinero o cómo lo ganaste.\n\n4. Clasifica la categoría en el menú desplegable (Comida, Salud, Transporte). Finalmente, haz clic en 'Guardar'. No tendrás que esperar, el gráfico central lo absorberá."
        ],
        "image": "docs/assets/add_movement_modal.png",
        "caption": "Figura 4. Formulario emergente para reportar gastos evitando perder de vista la situación general."
    },
    {
        "type": "chapter",
        "title": "CONSTRUCCIÓN EDUCATIVA 50/30/20",
        "content": [
            "APLICANDO INTELIGENCIA EN SUS INGRESOS:\nAl navegar al módulo 'Estudio/Educación' en el menú lateral de tu izquierda, el usuario notará que el sistema no es un simple archivador.\n\nLa herramienta tomará de forma inteligente todas las sumas depositadas mes a mes como ingresos y las recalculará inmediatamente mediante el principio financiero mundial recomendando reparticiones exactas: 50% Obligaciones Básicas, 30% Placer o Inversión, y el inquebrantable 20% para Fondo De Emergencia que salva hogares de quiebras rotundas."
        ],
        "image": "docs/assets/study_module.png",
        "caption": "Figura 5. Módulo interactivo de asimilación educativa de prioridades porcentuales."
    },
    {
        "type": "tip",
        "content": "Ajuste su cinturón consultando esta gráfica cada vez que adicione una nómina jugosa. Prevendrá gastarlo instintivamente en objetos de valor devaluativo."
    },
    {
        "type": "chapter",
        "title": "ADMINISTRACIÓN Y LIQUIDACIÓN DE DEUDAS",
        "content": [
            "EXPERIENCIA DE ALIVIO PATRIMONIAL:\nEl ítem 'Deudas' tiene una dedicación suprema en esta solución Web.\n\nSimplemente oprima 'Añadir' e inscriba a qué Institución u acreedor le debe capital (Ej. Tarjeta VISA). Asigne el Monto Original Total.\nAhora cada quincena, ingrese a esa deuda e ingrese un valor de un Abono a Capital. Visualmente verá como la barra espaciadora del panel se encoge, enviando un mensaje reforzador y positivo indicando su avance para quedar en estado Cero, Libre de embargos."
        ],
        "image": "docs/assets/debts_management.png",
        "caption": "Figura 6. Control pasivo minucioso mediante barra de mitigamiento crediticio progresivo real visual."
    },
    {
        "type": "chapter",
        "title": "PAGOS RUTINARIOS Y SUSCRIPCIONES (CALENDARIO)",
        "content": [
            "CALENDARIO PROGRAMADO DE EGRESOS INELUDIBLES:\nDentro de 'Pagos Fijos', la experiencia de navegación otorga tablas que le permitirán organizar suscripciones molestas (Streaming de Video) o pagos primarios (Tributos y Arriendos residenciales).\n\nAlinee sus facturas mes a mes e inclúyalas seleccionando una fecha de vencimiento y activando la repetición. Tendrá todo su panorama consolidado previniendo olvidos que conllevan moras e intereses gigantes."
        ],
        "image": "docs/assets/payments_page.png",
        "caption": "Figura 7. Tabular analítico programable de salidas constantes temporales. Nunca volverán sorpresas sobre su capital activo."
    },
    {
        "type": "chapter",
        "title": "ESTADO METEOROLÓGICO FINANCIERO: INTELIGENCIA GLOBAL",
        "content": [
            "OBSERVACIÓN EN TIEMPO REAL DEL MUNDO BURSÁTIL:\nIngresando al panel de noticias y rastreador en vivo en el apartado lateral inferior (News), el Aplicativo Web desglosa las tendencias globales e indicadores como Bitcoin y Divisas fuertes sin necesidad de abandonar la aplicación jamás.\n\nUsted como usuario logrará analizar si es momento de invertir su capital retenido sin incurrir en aplicaciones bancarias lentas u hostiles complejas especializadas. "
        ],
        "image": "docs/assets/news_module.png",
        "caption": "Figura 8. Interfaz analítica inteligente extraída en su propio observatorio."
    },
    {
        "type": "chapter",
        "title": "MODIFICACIÓN DE PERFIL Y AJUSTES",
        "content": [
            "CONTROL PLENO DE CREDENCIALES AL COSTADO:\nAl ir al ícono perimetral interior (Profile / Tools), la página proveerá cajas de inserción dinámicas transparentes de rápida mutación.\n\nAquí el cliente logrará renombrar y rotar nombres y credenciales evitando quedar anclado, proveyendo al aplicativo autonomía para reinicializar cuentas de ser precisado. También permite interconectar ajustes cromáticos y de husos horarios dependiendo del país en donde se encuentre ubicado el prestatario."
        ],
        "image": "docs/assets/profile_module.png",
        "caption": "Figura 9. Gestión profunda que centraliza a la persona y protege sus variables exógenas."
    },
    {
        "type": "chapter",
        "title": "VERIFICACIÓN DETALLADA: LECTURA DE GRÁFICOS",
        "content": [
            "INTERACCIÓN PROFUNDA CON EL PANEL CENTRAL:\nLa ventana principal del aplicativo no es estática. A medida que vayas integrando capital nuevo (salarios, abonos) o gastos, notarás que los gráficos toman forma. \n\nSi necesitas saber exactamente el monto o porcentaje de un registro en un día específico, sencillamente pasa tu ratón o dedo sobre la porción coloreada de la gráfica (Efecto Hover). Vas a notar cómo un globo emergente (Tooltip) salta a la pantalla detallando el valor monetario preciso, como se evidencia a la perfección en la demostración visual debajo."
        ],
        "image": "docs/assets/chart_hover.png",
        "caption": "Figura 10. Interacción subcelular con las gráficas, revelando montos precisos al posicionar el cursor sobre ellas."
    },
    {
        "type": "chapter",
        "title": "AJUSTE FINO: MODIFICACIÓN EN PROFUNDIDAD DE CARTERA",
        "content": [
            "EL CONTROL SECUNDARIO DE OBLIGACIONES:\nCuando te enfrentes a ventanas emergentes complejas como la creación y reajuste de pasivos (Tarjetas de Crédito y Préstamos), es vital llenar los apartados adecuadamente.\n\nAl oprimir 'Añadir Nueva' o el botón azul de modificación, la plataforma congelará el entorno trasero y expondrá una caja de inserción interactiva. En esta caja puedes ajustar montos si tus deudas sufrieron retasaciones o agregar nuevos acreedores. Al grabar, se genera instantáneamente un estado de progreso nuevo que se alinea a tu realidad física."
        ],
        "image": "docs/assets/debt_modal.png",
        "caption": "Figura 11. Modal interactivo crediticia en estado de redacción. Nótese el bloqueo oscuro de fondo que guía la vista del usuario."
    },
    {
        "type": "chapter",
        "title": "PERSONALIZACIÓN GLOBAL Y CONFORT NOCTURNO",
        "content": [
            "MODIFICANDO EL COMPORTAMIENTO PRINCIPAL DEL APLICATIVO:\nEl sistema debe adaptarse a ti, no tú a él. Ingresando a la rueda dentada lateral (Settings), la herramienta te entrega gobernanza total sobre cómo percibes la interfaz. ¿Cansado del brillo blanco puro que afecta la retina por la noche? Ubica el 'Interruptor' de Modo Oscuro y pulsa sobre el switch circular interactivo.\n\nTodo el sistema visual en una mínima fracción de segundo transmutará hacia tonalidades de azul profundo y negro mate (Dark Mode), optimizando la legibilidad para tu vista y transformando tu escritorio en un centro de mando ultra-profesional sin recargas molestas de página."
        ],
        "image": "docs/assets/settings_detail.png",
        "caption": "Figura 12. Demostración de accionamiento instantáneo del interruptor perimetral de sistema para control de entornos gráficos."
    },
    {
        "type": "chapter",
        "title": "CONCLUSIÓN E INDICACIONES FINALES",
        "content": [
            "Al dominar cada una de estas pestañas, un usuario novato se convierte rápidamente en un administrador nato y profesional de sus recursos de caja.\n\nSientase capacitado para accionar operaciones simultáneas. Todo lo descrito durante estas instrucciones guiadas reaccionan de inmediato con su teclado o su explorador convencional con una precisión incomparable."
        ]
    }
]

def generate():
    pdf = UserMegaManual(
        main_title="MANUAL ULTRA-DETALLADO DE USUARIO",
        subtitle="APLICATIVO WEB PARA FINANZAS PERSONALES",
        author="Guía de Navegación Operativa"
    )
    
    pdf.cover_and_index(sections)
    
    chap_num = 1
    for s in sections:
        if s["type"] == "chapter":
            pdf.add_page()
            pdf.chapter_title(str(chap_num), s["title"])
            chap_num += 1
            for p in s.get("content", []):
                pdf.chapter_body(p)
            if "image" in s:
                pdf.add_image(s["image"], s["caption"])
        elif s["type"] == "tip":
            pdf.tip_box(s["content"])
            
    pdf.output("Manual_Usuario_Mega_2026.pdf")
    print(f"Manual Generado: {pdf.page_no()} páginas.")

if __name__ == "__main__":
    generate()
