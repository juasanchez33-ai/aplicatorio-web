import os
import re
import subprocess
import base64
import commonmark

assets_dir = "assets"
md_file = "MANUAL_USUARIO.md"
html_file = os.path.abspath("MANUAL_USUARIO_BASE64.html")
pdf_file = os.path.abspath("MANUAL_DE_USUARIO_FINAL.pdf")

with open(md_file, "r", encoding="utf-8") as f:
    text = f.read()

def img_to_base64(filepath):
    if not os.path.exists(filepath): return ""
    with open(filepath, "rb") as image_file:
        enc = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{enc}"

# Reemplaza los corchetes por imagenes embedded reales
def replace_img(match):
    path = match.group(1).strip()
    b64 = img_to_base64(path)
    if b64:
        return f'<img src="{b64}" alt="Captura UX" width="100%" />'
    return f"*[IMAGEN NO ENCONTRADA: {path}]*"

text = re.sub(r'\[CAPTURA DE PANTALLA:\s*(.*?)\]', replace_img, text)

parser = commonmark.Parser()
ast = parser.parse(text)
renderer = commonmark.HtmlRenderer()
html_body = renderer.render(ast)

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
@page {{ margin: 0; }} /* REMOVE CHROME FILE:/// AND PAGES */

body {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
    font-size: 16pt;
    line-height: 1.8;
    color: #1e293b;
    padding: 60px 80px;
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
    font-size: 50pt;
    font-weight: 900;
    color: #0f172a;
    border: none;
    line-height: 1.2;
    text-transform: uppercase;
}}
.cover h2 {{
    font-size: 30pt;
    font-weight: 600;
    color: #0284c7;
    margin-top: 20px;
    border: none;
    background: transparent;
}}
h1 {{
    color: #0f172a;
    font-size: 32pt;
    border-bottom: 5px solid #10b981; /* Verde esmeralda para usuario */
    padding-bottom: 12px;
    margin-top: 50px;
    page-break-after: avoid;
}}
h2 {{
    color: #059669;
    font-size: 26pt;
    border-left: 10px solid #10b981;
    padding-left: 20px;
    background-color: #ecfdf5;
    padding-top: 20px;
    padding-bottom: 20px;
    margin-top: 60px;
    page-break-after: avoid;
}}
h3 {{
    color: #047857;
    font-size: 20pt;
    margin-top: 40px;
    page-break-after: avoid;
}}
p, span, div, li, td, th {{
    font-size: 18pt; /* Tamaño enorme y legible mantenido */
    line-height: 1.7;
    margin-bottom: 25px;
}}
li {{
    margin-bottom: 15px;
}}
img {{
    max-width: 95%;
    display: block;
    margin: 40px auto;
    border: 3px solid #e2e8f0;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}}
.page-divider {{
    page-break-before: always;
    padding-top: 20px;
}}
hr {{
    border: top 2px solid #cbd5e1;
    margin: 40px 0;
}}
</style>
</head>
<body>
<div class="cover">
    <h1>Aplicativo Web para el Manejo de Finanzas Personales</h1>
    <h2>Manual del Usuario</h2>
</div>
{html_body}
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML User Manual guardado.")

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
    print(f"¡PDF Generado en: {pdf_file}!")
