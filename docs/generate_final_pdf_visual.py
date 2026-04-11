import os
import re
import subprocess
import commonmark

# Configuration
input_md = "MANUAL_TECNICO_MAESTRO_OMEGA.md"
output_html = os.path.abspath("OMEGA_PRINT_READY.html")
output_pdf = os.path.abspath("MANUAL_TECNICO_MAESTRO_OMEGA_FINAL.pdf")

# Read MD
with open(input_md, "r", encoding="utf-8") as f:
    content = f.read()

# Extract embedded style if any, but since we'll just convert MD to HTML 
# and wrap it, commonmark will handle the <div> and <img> tags fine.

# Convert MD to HTML body
parser = commonmark.Parser()
ast = parser.parse(content)
renderer = commonmark.HtmlRenderer()
html_body = renderer.render(ast)

# Wrap in full HTML document
# Note: We don't add styles here because they are ALREADY in the Markdown file!
# We just need to make sure paths are absolute for Chrome.
base_path = os.path.abspath(".").replace("\\", "/")
html_body = html_body.replace('src="assets/', f'src="file:///{base_path}/assets/')

full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Manual Técnico Maestro OMEGA</title>
    <!-- Mermaid script to render diagrams -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    <style>
        @page {{
            margin: 0;
            size: A4;
        }}
        body {{
            margin: 0;
            padding: 0;
            background: white;
        }}
        /* Mermaid Diagram Centering */
        .mermaid {{
            display: flex;
            justify-content: center;
            margin: 60px 0;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

with open(output_html, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"HTML intermedio generado: {output_html}")

# Find Chrome
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
    print(f"Generando PDF usando {selected_chrome}...")
    args = [
        selected_chrome,
        "--headless",
        "--disable-gpu",
        "--print-to-pdf-no-header",
        "--enable-logging",
        "--no-sandbox",
        f"--print-to-pdf={output_pdf}",
        output_html
    ]
    subprocess.run(args)
    print(f"¡ÉXITO! PDF Generado: {output_pdf}")
else:
    print("ERROR: No se encontró Google Chrome para la exportación.")
