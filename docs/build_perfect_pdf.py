import commonmark
import os
import re
import subprocess

md_file = "MANUAL_TECNICO_PROFESIONAL.md"
html_file = os.path.abspath("MANUAL_FINAL_CORREGIDO.html")
pdf_file = os.path.abspath("MANUAL_TECNICO_FINAL_PERFECTO.pdf")

with open(md_file, "r", encoding="utf-8") as f:
    text = f.read()

# 1. BORRAR BLOQUE DE ESTILO
text = re.sub(r'<style>.*?</style>', '', text, flags=re.DOTALL)

# 2. BORRAR EL TÍTULO "FIN DEL MANUAL TECNICO" Y LO QUE LE SIGA
text = re.split(r'###\s*FIN DEL MANUAL', text, flags=re.IGNORECASE)[0]
text = re.split(r'###\s*FIN DE LA ESPECIFICACI', text, flags=re.IGNORECASE)[0]

# 3. LIMPIAR EL TÍTULO ORIGINAL (Para hacer nosotros la portada pura)
text = re.sub(r'# TÍTULO:.*?\n', '', text, flags=re.IGNORECASE)

# 4. INYECTAR LAS IMÁGENES TANGO EN LOS PLACEHOLDERS ORIGINALES
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/login_page.png]", "![Login Segurizado](assets/login_page_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/add_movement_modal.png]", "![Registro Movimiento](assets/add_movement_modal_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/dashboard_main.png]", "![Dashboard Principal](assets/dashboard_main_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/study_module.png]", "![Módulo Educación](assets/study_module_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/debts_management.png]", "![Gestión Deudas](assets/debts_management_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/payments_page.png]", "![Pagos Fijos](assets/payments_page_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/profile_module.png]", "![Perfil de Usuario](assets/profile_module_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/chart_hover.png]", "![Interacción Gráfico](assets/chart_hover_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/debt_modal.png]", "![Deuda Creada](assets/debt_modal_tango.png)")
text = text.replace("[CAPTURA DE PANTALLA: /docs/assets/settings_detail.png]", "![Configuracion UI](assets/settings_detail_tango.png)")

# En su caso, hay corchetes como [CAPTURA DE PANTALLA: /.../archivo.png] que pueden sobrar
text = re.sub(r'\[CAPTURA DE PANTALLA:.*?\]', '', text)

# Hacer paths absolutos
text = text.replace("](assets/", f"](file:///{os.path.abspath('assets')}/".replace('\\', '/'))

parser = commonmark.Parser()
ast = parser.parse(text)
renderer = commonmark.HtmlRenderer()
html_body = renderer.render(ast)

# LA PÁGINA 1 VA A SER SÓLO EL TÍTULO CENTRADO CON NADA MÁS. LUEGO SALTO DE PÁGINA.
html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700;900&display=swap');
body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 18pt; /* TAMAÑO DE LETRA ELEVADO SIGNIFICATIVAMENTE PARA LECTURA FÁCIL */
    line-height: 1.7;
    color: #1e293b;
    margin: 40px;
}}

/* ESTILOS DE LA PORTADA EXCLUSIVA */
.cover {{
    height: 90vh; /* Ocupar página completa */
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    page-break-after: always;
}}
.cover h1 {{
    font-size: 50pt;
    font-weight: 900;
    color: #0f172a;
    border: none;
    line-height: 1.2;
    text-transform: uppercase;
    margin: 0;
    padding: 0;
}}

/* CONTENIDO GENERAL */
h1 {{
    color: #0f172a;
    font-size: 32pt;
    border-bottom: 5px solid #00f0ff;
    padding-bottom: 12px;
    margin-top: 50px;
    page-break-after: avoid;
}}
h2 {{
    color: #0284c7;
    font-size: 26pt;
    border-left: 10px solid #00f0ff;
    padding-left: 20px;
    background-color: #f0f9ff;
    padding-top: 20px;
    padding-bottom: 20px;
    margin-top: 60px;
    page-break-after: avoid;
}}
h3 {{
    color: #0284c7;
    font-size: 22pt;
    margin-top: 40px;
    page-break-after: avoid;
}}
p, span, div, li, td, th {{
    font-size: 18pt;
    line-height: 1.7;
}}
p {{
    margin-bottom: 25px;
    text-align: justify;
}}
li {{
    margin-bottom: 15px;
}}
pre {{
    background-color: #0f172a;
    color: #f8fafc;
    padding: 25px;
    border-radius: 12px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13pt; /* AUMENTADO PARA LEGIBILIDAD EXTREMA */
    line-height: 1.5;
    white-space: pre-wrap;     /* Fix code wrapping */
    word-break: break-all;     /* Fix long lines */
    page-break-inside: avoid;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}}
code {{
    background-color: #e2e8f0;
    color: #b91c1c;
    padding: 2px 8px;
    border-radius: 6px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 15pt;
}}

/* SECCIÓN IMÁGENES */
img {{
    max-width: 90%;
    height: auto;
    display: block;
    margin: 60px auto; /* Mayor distancia para separar secciones */
    border: 3px solid #e2e8f0;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}}
.page-divider {{
    page-break-before: always;
}}
blockquote {{
    padding: 25px;
    background-color: #eff6ff;
    border-left: 10px solid #3b82f6;
    margin: 40px 0;
    border-radius: 10px;
    font-style: italic;
    page-break-inside: avoid;
}}
hr {{
    border: none;
    border-top: 3px solid #cbd5e1;
    margin: 50px 0;
}}
</style>
</head>
<body>

<div class="cover">
    <h1>Aplicativo Web para el Manejo de Finanzas Personales</h1>
</div>

{html_body}

</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML formateado guardado: {html_file}")

chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]
selected_chrome = None
for p in chrome_paths:
    if os.path.exists(p):
        selected_chrome = p
        break

if selected_chrome:
    args = [
        selected_chrome,
        "--headless",
        "--disable-gpu",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]
    subprocess.run(args)
    print(f"¡PDF generado con éxito en: {pdf_file}!")
else:
    print("NO SE ENCONTRÓ CHROME.")
