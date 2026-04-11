import commonmark
import os
import subprocess

md_file = "MANUAL_UNIFICADO_TANGO.md"
html_file = os.path.abspath("MANUAL_FINAL.html")
pdf_file = os.path.abspath("MANUAL_TECNICO_FINAL_PERFECTO.pdf")

if not os.path.exists(md_file):
    print("Cannot find unificado file. Creating a dummy for now.")
    with open(md_file, "w") as f: f.write("# Error")

with open(md_file, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("](assets/", f"](file:///{os.path.abspath('assets')}/".replace('\\', '/'))

parser = commonmark.Parser()
ast = parser.parse(text)
renderer = commonmark.HtmlRenderer()
html_body = renderer.render(ast)

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 14pt;
    line-height: 1.6;
    color: #1e293b;
    margin: 40px;
}}
p, span, div, li, td, th {{
    font-size: 14pt;
    line-height: 1.6;
}}
h1 {{
    color: #0f172a;
    font-size: 28pt;
    border-bottom: 4px solid #00f0ff;
    padding-bottom: 10px;
    margin-top: 60px;
    page-break-after: avoid;
}}
h2 {{
    color: #0369a1;
    font-size: 20pt;
    border-left: 8px solid #00f0ff;
    padding-left: 15px;
    background-color: #f0f9ff;
    padding-top: 15px;
    padding-bottom: 15px;
    margin-top: 50px;
    page-break-after: avoid;
}}
h3 {{
    color: #0284c7;
    font-size: 16pt;
    margin-top: 30px;
    page-break-after: avoid;
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
    padding: 20px;
    border-radius: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 10pt;
    line-height: 1.4;
    white-space: pre-wrap;     /* Fixes code wrapping off-screen */
    word-break: break-all;     /* Fixes extremely long lines */
    page-break-inside: avoid;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}}
code {{
    background-color: #e2e8f0;
    color: #b91c1c;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 11pt;
}}
img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 40px auto;
    border: 2px solid #cbd5e1;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}
.page-divider {{
    page-break-before: always;
}}
blockquote {{
    padding: 20px;
    background-color: #eff6ff;
    border-left: 8px solid #3b82f6;
    margin: 30px 0;
    border-radius: 8px;
    font-style: italic;
    page-break-inside: avoid;
}}
hr {{
    border: none;
    border-top: 2px solid #cbd5e1;
    margin: 40px 0;
}}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML guardado. Ejecutando Chrome headless para renderizar PDF en alta calidad...")

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
    print(f"¡PDF generado exitosamente en {pdf_file}!")
else:
    print("NO SE ENCONTRÓ CHROME.")
