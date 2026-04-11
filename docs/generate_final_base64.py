import os
import re
import subprocess
import base64
import commonmark

assets_dir = "assets"
md_file = "MANUAL_TECNICO_PROFESIONAL.md"
html_file = os.path.abspath("MANUAL_BASE64.html")
pdf_file = os.path.abspath("MANUAL_TECNICO_FINAL_IMAGENES.pdf")

with open(md_file, "r", encoding="utf-8") as f:
    text = f.read()

text = re.sub(r'<style>.*?</style>', '', text, flags=re.DOTALL)
text = re.split(r'###\s*FIN DEL MANUAL', text, flags=re.IGNORECASE)[0]

def img_to_base64(filepath):
    if not os.path.exists(filepath): return ""
    with open(filepath, "rb") as image_file:
        enc = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{enc}"

visual_section = """
<div class="page-divider"></div>

# SECCIÓN VISUAL EXPLICATIVA: CADA PANTALLA EXPLICADA AL TÉCNICO

A continuación, se detalla el funcionamiento interno y visual de las capturas clave del sistema (utilizando el formato Tango especificado):

"""

explanations = {
    "login_page_tango.png": ("Módulo de Autenticación", "La vista frontal actúa como barrera preventiva. Los inputs detectan inyección SQL pasivamente gracias a la sanitización en Jinja2. Al ejecutar la acción de ingreso, se activa un protocolo Fetch asíncrono para despachar correos."),
    "register_page_tango.png": ("Registro de Usuarios Nuevos", "La creación de cuentas solicita nombre, correo y contraseña. A nivel de arquitectura, las credenciales son recibidas por el endpoint de FastAPI, y antes de insertar en la tabla SQLite `user_profiles`, se exige robustez de red."),
    "dashboard_main_tango.png": ("Dashboard Financiero Central", "El panel principal. Aquí JavaScript iterativo recibe el JSON agregado desde `/api/movements`. Las sumas o sustracciones se grafican iterativamente con librerías nativas usando el canvas dinámico HTML5."),
    "add_movement_modal_tango.png": ("Sistema de Ingesta de Capital", "El formulario modal que interrumpe la pantalla (zIndex alto). Al escribir el monto, la API inyecta el `payload` hacia SQLite (Tabla `movements`), y devuelve un OK(200) que provoca el recargo gráfico transparente."),
    "debts_management_tango.png": ("Amortizador de Pasivos", "Esta interfaz despliega un listado de obligaciones activas. Visualmente la barra de progreso decrece en línea con los cálculos aritméticos en el Python backend. La mutación en BD altera `paid_amount`."),
    "study_module_tango.png": ("Regla 50/30/20 Educativa", "La ventana de educación recoge la totalidad de ingresos brutos y los expone mediante multiplicadores flotantes de `0.5`, `0.3` y `0.2`. El proceso de renderizado no castiga al servidor, se hace en el cliente (Client-Side)."),
    "payments_page_tango.png": ("Suscripciones y Pagos Fijos", "Panel tabular de ciclo recurrente. Se enlaza a la tabla `payments`. Visualmente indica advertencias cuando la fecha de cobro cruza el diferencial de `datetime.now()` en la lógica Python."),
    "profile_module_tango.png": ("Configuraciones de Entidad", "Ajuste numérico y perfil. Las variables aquí modificadas se graban sobre `user_profiles` utilizando sentencias SQL transaccionales (`ON CONFLICT DO UPDATE`) previniendo duplicidad de llaves primarias en correos."),
    "settings_page_tango.png": ("Preferencias Generales y Dark Mode", "La opción visual de cambiar temas está inyectada en eventos JavaScript, modificando la variable maestra CSS y añadiendo persistencia en LocalStorage, por ende el cambio a la base de datos es opcional pero respaldado para MFA."),
}

for img_name, (title, desc) in explanations.items():
    full_path = os.path.join(assets_dir, img_name)
    if os.path.exists(full_path):
        b64 = img_to_base64(full_path)
        visual_section += f"## {title}\n"
        visual_section += f'<img src="{b64}" alt="{title}" width="100%" />\n'
        visual_section += f"\n**Explicación Técnica del Despliegue:**\n{desc}\n\n"

text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
text = text + "\n" + visual_section

parser = commonmark.Parser()
ast = parser.parse(text)
renderer = commonmark.HtmlRenderer()
html_body = renderer.render(ast)

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700;900&display=swap');
@page {{ margin: 0; }} /* ESTO ELIMINA EL FOOTER Y EL HEADER DE FILE:// MÁS NUMEROS DE PAGINA AUTOMATICOS DE CHROME */

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16pt;
    line-height: 1.8;
    color: #1e293b;
    padding: 60px 80px; /* AL RETIRAR EL MARGEN DE PÁGINA, SE SUPLE CON PADDING DE BODY PARA NO PERDER LA ESTRUCTURA */
    box-sizing: border-box;
}}
.cover {{
    height: 90vh;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    page-break-after: always;
}}
.cover h1 {{
    font-size: 55pt;
    font-weight: 900;
    color: #0f172a;
    border: none;
    line-height: 1.2;
    text-transform: uppercase;
}}
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
p, span, div, li, td, th {{
    font-size: 16pt;
    line-height: 1.8;
}}
pre {{
    background-color: #0f172a;
    color: #f8fafc;
    padding: 25px;
    border-radius: 12px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12pt;
    white-space: pre-wrap;
    word-break: break-all;
    page-break-inside: avoid;
}}
code {{
    background-color: #e2e8f0;
    color: #b91c1c;
    padding: 2px 8px;
    border-radius: 6px;
    font-family: 'Consolas', 'Courier New', monospace;
}}
img {{
    max-width: 95%;
    display: block;
    margin: 40px auto;
    border: 3px solid #e2e8f0;
    border-radius: 12px;
}}
.page-divider {{
    page-break-before: always;
    padding-top: 20px;
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

print(f"HTML Base64 guardado.")

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
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]
    subprocess.run(args)
    print(f"¡NUEVO PDF GENERADO EN: {pdf_file}!")
