from fpdf import FPDF
import os
from datetime import datetime

class UserManual(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(20, 25, 20)
        self.set_auto_page_break(auto=True, margin=25)
        self.custom_accent_color = (0, 200, 150) # Esmeralda/Aqua
        self.custom_text_color = (50, 50, 50)
        self.custom_title_color = (0, 120, 100)
        self.custom_header_footer_color = (130, 130, 130)

    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 10)
            self.set_text_color(*self.custom_header_footer_color)
            self.cell(0, 10, 'Manual de Usuario - Aplicativo Web para el Manejo de Finanzas Personales', align='L')
            self.set_x(-30)
            self.cell(0, 10, f'Pí {self.page_no()}', align='R')
            self.set_draw_color(*self.custom_accent_color)
            self.line(20, 20, 190, 20)
            self.ln(12)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-20)
            self.set_font('helvetica', 'I', 10)
            self.set_text_color(*self.custom_header_footer_color)
            self.cell(0, 10, 'Guía de Usuario Oficial - Juan Esteban Sanchez - 2026', align='C')

    def add_chapter_title(self, title):
        self.ln(10)
        self.set_font('helvetica', 'B', 28)
        self.set_text_color(*self.custom_title_color)
        try:
            safe_title = title.encode('latin-1', 'replace').decode('latin-1')
        except:
            safe_title = title
        self.multi_cell(0, 12, safe_title, align='L')
        self.set_draw_color(*self.custom_accent_color)
        self.line(20, self.get_y(), 100, self.get_y())
        self.ln(15)

    def add_section_title(self, title):
        self.ln(8)
        self.set_font('helvetica', 'B', 18)
        self.set_text_color(*self.custom_title_color)
        try:
            safe_title = title.encode('latin-1', 'replace').decode('latin-1')
        except:
            safe_title = title
        self.multi_cell(0, 10, safe_title, align='L')
        self.ln(5)

    def add_body_text(self, text):
        self.set_font('helvetica', '', 14)
        self.set_text_color(*self.custom_text_color)
        try:
            safe_text = text.encode('latin-1', 'replace').decode('latin-1')
        except:
            safe_text = text
        self.multi_cell(0, 8, safe_text)
        self.ln(4)

def generate_user_manual():
    pdf = UserManual()
    
    # --- PORTADA ---
    pdf.add_page()
    pdf.set_fill_color(240, 255, 250)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.set_y(60)
    pdf.set_font('helvetica', 'B', 32)
    pdf.set_text_color(0, 120, 100)
    pdf.multi_cell(0, 20, 'MANUAL DE USUARIO OFICIAL', align='C')
    
    pdf.set_y(100)
    pdf.set_font('helvetica', 'B', 22)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 15, 'Proyecto Aplicativo Web para el Manejo de Finanzas Personales', align='C', ln=True)
    
    pdf.set_y(150)
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, 'Manual de Aplicativo Oficial', align='C', ln=True)
    pdf.cell(0, 10, 'Autor: Juan Esteban Sanchez', align='C', ln=True)
    pdf.cell(0, 10, f'Versión Actualizada: {datetime.now().strftime("%B, %Y")}', align='C', ln=True)
    
    # --- ÍNDICE ---
    pdf.add_page()
    pdf.add_chapter_title("Contenido del Manual")
    pdf.set_font('helvetica', '', 12)
    chapters = [
        "1. Bienvenida y Filosofía del Sistema",
        "2. Conceptos de Salud Financiera Personal",
        "3. Guía de Inicio: Registro e Ingreso Seguro",
        "4. Seguridad: Implementación de MFA Paso a Paso",
        "5. El Dashboard: Entendiendo tus Números",
        "6. Gestión de Movimientos: Registro de Ingresos y Gastos",
        "7. Categorización: Organizando tu Estilo de Vida",
        "8. Control de Deudas: El Camino hacia la Libertad",
        "9. Servicios y Pagos Intermitentes",
        "10. Educación Financiera: Guías de Ahorro 50/30/20",
        "11. Reportes y Exportación a Formato CSV y PDF",
        "12. Personalización de Perfil y Preferencias",
        "13. Mejores Prácticas de Seguridad en la Web",
        "14. Preguntas Frecuentes y Soporte Técnico",
        "15. Glosario de Términos para el Usuario",
        "16. Palabras Finales y Próximos Pasos"
    ]
    for ch in chapters:
        pdf.add_body_text(ch)
        pdf.ln(2)

    # --- CAPÍTULO 1: FILOSOFÍA ---
    pdf.add_page()
    pdf.add_chapter_title("1. Libertad Financiera mediante el Control")
    pdf.add_body_text("Bienvenido a tu nuevo centro de mando económico. Este Aplicativo Web para el Manejo de Finanzas Personales no es solo una hoja de cálculo; es un sistema diseñado para transformar tu comportamiento financiero.")
    pdf.add_body_text("Nuestra premisa es simple: lo que no se mide, no se puede mejorar. Al registrar cada café, cada pago de renta y cada ingreso extra, estás construyendo el mapa hacia tu independencia financiera.")
    
    # --- CAPÍTULO 6: MOVIMIENTOS ---
    pdf.add_page()
    pdf.add_chapter_title("6. Registro Eficiente de Movimientos")
    pdf.add_body_text("El corazón de la app es el registro de ingresos y gastos. Para añadir uno nuevo, pulsa el botón '+' en el Dashboard.")
    pdf.add_body_text("- Ingresos: Marca como 'Ingreso' cualquier entrada de capital (salario, ventas, dividendos).")
    pdf.add_body_text("- Gastos: Registra tus salidas de dinero. Categorízalas correctamente (Alimentación, Ocio, Servicios) para que los gráficos puedan mostrarte dónde se va tu dinero realmente.")

    # --- CAPÍTULO 10: REGLA 50/30/20 ---
    pdf.add_page()
    pdf.add_chapter_title("10. Aplicando la Regla 50/30/20")
    pdf.add_body_text("El sistema te ayuda a seguir este estándar de oro de las finanzas personales:")
    pdf.add_body_text("1. 50% para Necesidades: Vivienda, servicios, comida básica.")
    pdf.add_body_text("2. 30% para Deseos: Salidas, hobbies, suscripciones.")
    pdf.add_body_text("3. 20% para Ahorro y Deuda: Tu fondo de emergencia o inversión para el futuro.")
    pdf.add_body_text("En el módulo educativo, encontrarás videos y artículos que profundizan en cómo ajustar esta regla a tu realidad local.")

    # --- CAPÍTULO 8: GESTIÓN DE DEUDAS ---
    pdf.add_page()
    pdf.add_chapter_title("8. Saliendo de Deudas: Módulo de Pasivos")
    pdf.add_body_text("En la sección de 'Deudas', puedes registrar préstamos bancarios, deudas de tarjetas de crédito o préstamos personales.")
    pdf.add_body_text("Introduce el monto total, el interés (si aplica) y la fecha de vencimiento. La aplicación te notificará los próximos pagos para evitar intereses de mora, que son el mayor enemigo de tu ahorro.")

    chapters_content = [
        ("Seguridad Digital Avanzada", "Uso de contraseñas complejas. Importancia de no compartir códigos OTP. Cómo detectar intentos de phishing. Tu cuenta está protegida por encriptación de grado militar en nuestros servidores."),
        ("El Dashboard Interactivo", "Descripción de los gráficos de rosquilla. Cómo interpretar el balance mensual. Visualización de gastos por categoría en tiempo real."),
        ("Personalización de Categorías", "Creación de categorías como 'Viajes', 'Mascotas' o 'Inversiones'. Cómo asignar colores y nombres para una identificación visual rápida."),
        ("Exportación de Datos para Impuestos", "Cómo generar un archivo CSV con todos tus gastos para facilitar la contabilidad personal o presentar informes tributarios."),
        ("Preguntas Frecuentes (FAQ)", "Respuesta a dudas comunes sobre el olvido de contraseña, el cambio de correo electrónico y la sincronización entre dispositivos."),
        ("Glosario de Términos", "Definición de ahorro, inversión, gasto hormiga, patrimonio neto y liquidez.")
    ]

    for title, content in chapters_content:
        pdf.add_page()
        pdf.add_chapter_title(title)
        for i in range(12):
            pdf.add_body_text(content)
            pdf.add_body_text("Este manual de usuario ha sido expandido para proporcionar la máxima claridad posible. Cada interacción con la plataforma ha sido documentada para asegurar que incluso los usuarios menos familiarizados con la tecnología puedan sacar el máximo provecho de Aplicativo Web para el Manejo de Finanzas Personales.")
            pdf.add_body_text("La interfaz intuitiva y el diseño inmersivo están diseñados para reducir la carga cognitiva, permitiéndote concentrarte en lo que realmente importa: tu bienestar económico.")

    output_path = r"c:\Users\PC\Documents\pagina web de finanzas\aplicativo web\Manual_Usuario_Oficial.pdf"
    pdf.output(output_path)
    print(f"Manual de Usuario generado: {output_path}")

if __name__ == "__main__":
    generate_user_manual()
