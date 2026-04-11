import commonmark
from fpdf import FPDF, HTMLMixin
import os

class PDF(FPDF, HTMLMixin):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'Manual Tecnico Profesional - Finanzas Web', border=False, align='C')
        self.line(10, 20, 200, 20)
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

# Edit the markdown to use the _tango images and fix the placeholder synatx
md_path = "MANUAL_TECNICO_PROFESIONAL.md"
with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace placeholders with markdown image syntax
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/login_page.png]", "![Captura Login](assets/login_page_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/add_movement_modal.png]", "![Captura Gasto](assets/add_movement_modal_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/dashboard_main.png]", "![Captura Dashboard](assets/dashboard_main_tango.png)")

# Remove CSS section
if "<style>" in text:
    text = text.split("</style>")[1].strip()

# Hack for alerts (commonmark doesn't support GH alerts natively easily, we'll convert them to bold quotes)
text = text.replace("> [!CAUTION]", "> **[ ! ] ADVERTENCIA DE SEGURIDAD:**")
text = text.replace("> [!TIP]", "> **[ ! ] CONSEJO TÉCNICO:**")

parser = commonmark.Parser()
ast = parser.parse(text)
renderer = commonmark.HtmlRenderer()
html = renderer.render(ast)

pdf = PDF()
pdf.add_font("Arial", "", "c:/windows/fonts/arial.ttf")
pdf.add_font("Arial", "B", "c:/windows/fonts/arialbd.ttf")
pdf.add_font("Arial", "I", "c:/windows/fonts/ariali.ttf")
pdf.add_page()
pdf.set_font('Arial', '', 12)

# Insert the HTML into PDF
# FPDF2 HTMLMixin supports a lot of standard tags
try:
    pdf.write_html(html)
except Exception as e:
    print(f"Error HTML: {e}")
    # Fallback just write text
    pdf.add_page()
    pdf.multi_cell(0, 10, txt="Fallo leido de HTML.")
    
output_file = "MANUAL_TECNICO_FINAL_TANGO.pdf"
pdf.output(output_file)
print(f"Generado {output_file} exitosamente.")
