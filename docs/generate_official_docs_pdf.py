import os
import re
import subprocess
import base64
import commonmark

assets_dir = "assets"
md_file = "DOCUMENTACION_OFICIAL_ULTRA_DENSA.md"
html_file = os.path.abspath("DOCUMENTACION_OFICIAL_BASE64.html")
pdf_file = os.path.abspath("DOCUMENTACION_OFICIAL_SISTEMA.pdf")

def img_to_base64(filepath):
    # Intentar varias rutas relativas comunes
    search_paths = [
        filepath,
        os.path.join("..", "app", "static", "img", os.path.basename(filepath)),
        os.path.join("app", "static", "img", os.path.basename(filepath)),
        os.path.join(assets_dir, os.path.basename(filepath))
    ]
    for p in search_paths:
        if os.path.exists(p):
            with open(p, "rb") as image_file:
                enc = base64.b64encode(image_file.read()).decode("utf-8")
                return f"data:image/png;base64,{enc}"
    return ""

with open(md_file, "r", encoding="utf-8") as f:
    text = f.read()

# Replace image placeholders
def replace_img(match):
    path = match.group(1).strip().replace("/docs/", "")
    b64 = img_to_base64(path)
    if b64:
        return f'<div class="img-wrapper"><img src="{b64}" alt="Figura Técnica" /><p class="img-description">Ilustración: {os.path.basename(path)}</p></div>'
    return f"*[IMAGEN NO ENCONTRADA: {path}]*"

text = re.sub(r'\[CAPTURA DE PANTALLA:\s*(.*?)\]', replace_img, text)
text = re.sub(r'!\[.*?\]\((.*?)\)', replace_img, text)

parser = commonmark.Parser()
ast = parser.parse(text)
renderer = commonmark.HtmlRenderer()
html_body = renderer.render(ast)

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=Inter:wght@400;600;800&display=swap');
@page {{ margin: 3cm; }} 

body {{
    font-family: 'Crimson Pro', serif;
    font-size: 18pt; /* Aumento a 18pt para legibilidad extrema */
    line-height: 2.0; /* Interlineado aumentado para mayor volumen */
    color: #1a1a1a;
    padding: 0;
    margin: 0;
    text-align: justify;
    background: #ffffff;
}}

/* PORTADA DE TESIS CORPORATIVA - FIJANDO ALTURA PARA EVITAR DESBORDAMIENTO */
.thesis-cover {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    height: 100vh;
    padding: 2cm 2cm;
    page-break-after: always;
    box-sizing: border-box;
    overflow: hidden;
}}

.univ-name {{
    font-family: 'Inter', sans-serif;
    font-size: 20pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.3cm;
    color: #000;
    margin-bottom: 2cm;
}}

.doc-main-heading {{
    font-family: 'Inter', sans-serif;
    font-size: 30pt;
    font-weight: 900;
    margin: 1cm 0;
    line-height: 1.1;
    color: #000;
    text-transform: uppercase;
}}

.subtitle {{
    font-family: 'Inter', sans-serif;
    font-size: 18pt;
    font-weight: 500;
    color: #334155;
    margin-bottom: 4cm;
}}

.bottom-meta {{
    font-family: 'Inter', sans-serif;
    font-size: 14pt;
    font-weight: 600;
    color: #000;
    margin-top: auto;
}}

/* ESTILOS DE CUERPO DENSE */
h1 {{
    font-family: 'Inter', sans-serif;
    font-size: 28pt;
    font-weight: 800;
    color: #000;
    border-bottom: 3pt solid #000;
    padding-bottom: 0.5cm;
    margin-top: 4cm;
    page-break-before: always;
    text-transform: uppercase;
}}
h2 {{
    font-family: 'Inter', sans-serif;
    font-size: 22pt;
    font-weight: 700;
    color: #000;
    margin-top: 2.5cm;
    margin-bottom: 1.2cm;
}}
h3 {{
    font-family: 'Inter', sans-serif;
    font-size: 18pt;
    font-weight: 600;
    color: #222;
    margin-top: 2cm;
}}
a {{
    color: #0891b2;
    text-decoration: none;
    font-weight: 700;
}}
p {{
    margin-bottom: 0.8cm;
    orphans: 3;
    widows: 3;
}}
.img-wrapper {{
    text-align: center;
    margin: 2cm 0;
    page-break-inside: avoid;
}}
img {{
    max-width: 85%;
    border: 1pt solid #000;
}}
.img-description {{
    font-size: 10pt;
    color: #666;
    margin-top: 0.5cm;
    font-style: italic;
}}
pre {{
    font-family: 'Consolas', monospace;
    font-size: 10pt;
    background: #fbfbfb;
    border: 0.5pt solid #000;
    padding: 1cm;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 1cm 0;
    page-break-inside: avoid;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1.5cm 0;
}}
th, td {{
    border: 0.5pt solid #000;
    padding: 0.3cm;
    font-size: 10pt;
}}
th {{
    background: #f0f0f0;
}}
.page-divider {{
    page-break-before: always;
}}
</style>
</head>
<body>

<div class="thesis-cover">
    <div class="univ-name">Universidad Antonio Nariño</div>
    <div class="doc-main-heading">DOCUMENTACIÓN OFICIAL</div>
    <div class="subtitle">Aplicativo web para el manejo de finanzas personales</div>
    
    <div class="bottom-meta">
        JUAN ESTEBAN SANCHEZ<br>
        Facultad de Ingeniería de Software | 2026
    </div>
</div>

<div class="doc-body">
{html_body}
</div>

</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

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
    print(f"EXITO: Documentación Maestro de Ingeniería Generada.")
else:
    print("ERROR: No se encontró Chrome.")
