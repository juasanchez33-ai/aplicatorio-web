import os
import re

file1 = "MANUAL_TECNICO_ACADEMICO.md"
file2 = "MANUAL_TECNICO_PROFESIONAL.md"
output_file = "MANUAL_UNIFICADO_TANGO.md"

with open(file1, "r", encoding="utf-8") as f:
    text1 = f.read()

with open(file2, "r", encoding="utf-8") as f:
    text2 = f.read()

# Strip out inline style blocks to avoid CSS conflicts, as we will use tango-style.css
text1 = re.sub(r'<style>.*?</style>', '', text1, flags=re.DOTALL)
text2 = re.sub(r'<style>.*?</style>', '', text2, flags=re.DOTALL)

# Also there's some HTML injected in the academic one, we can leave the divs as md-to-pdf parses HTML well.
combined_text = f"{text1}\n\n<div class='page-divider'></div>\n\n{text2}"

# Ensure Tango images points correctly
combined_text = combined_text.replace("[CAPTURA DE PANTALLA: /docs/assets/login_page.png]", "![Captura Login](assets/login_page_tango.png)")
combined_text = combined_text.replace("[CAPTURA DE PANTALLA: /docs/assets/add_movement_modal.png]", "![Captura Gasto](assets/add_movement_modal_tango.png)")
combined_text = combined_text.replace("[CAPTURA DE PANTALLA: /docs/assets/dashboard_main.png]", "![Captura Dashboard](assets/dashboard_main_tango.png)")

# If there is any markdown placeholder not explicitly defined with Tango, we should convert it to an image
def replace_unmapped_screenshots(match):
    path = match.group(1).replace("/docs/", "")
    return f"![Captura]({path})"

combined_text = re.sub(r'\[CAPTURA DE PANTALLA:\s*(.*?)\]', replace_unmapped_screenshots, combined_text)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(combined_text)

print(f"Archivos unificados exitosamente en {output_file}")
