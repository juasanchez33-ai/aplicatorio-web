import re
import os

md_file = "MANUAL_UNIFICADO_TANGO.md"
with open(md_file, "r", encoding="utf-8") as f:
    text = f.read()

# Remove old placeholders to avoid duplicates
text = re.sub(r'!\[.*?\]\(.*?_tango\.png\)', '', text)

# Map sections to corresponding image hashes
injections = {
    "1.4. Análisis de Usuario": "![Perfil de Usuario](assets/profile_module_tango.png)",
    "3.2. Diagramación de Flujos de Datos": "![Arquitectura y Login](assets/login_page_tango.png)",
    "7.1 Módulo Cero: Autenticación y Despacho OTP": "![Pantalla Login](assets/login_page_tango.png)",
    "7.2 Módulo de Movimientos y Rutas": "![Gasto Modal](assets/add_movement_modal_tango.png)",
    "Módulo Analítico Global (Dashboard)": "![Dashboard Principal](assets/dashboard_main_tango.png)",
    "Amortizador de Deudas": "![Gestión de Deudas](assets/debts_management_tango.png)",
    "Educación 50/30/20": "![Módulo de Estudio](assets/study_module_tango.png)",
    "Exportador General de Inteligencia": "![Gestión Documental](assets/recover_page_tango.png)", 
    "Sistematizar Suscripciones (Pagos Fijos)": "![Pagos y Suscripciones](assets/payments_page_tango.png)",
    "Habilitar Exportación Táctica": "![Ajustes Generales](assets/settings_page_tango.png)",
}

for key, img_md in injections.items():
    if key in text:
        text = text.replace(key, f"{key}\n\n<div style='text-align: center; margin: 30px 0;'>{img_md}</div>\n\n")

with open(md_file, "w", encoding="utf-8") as f:
    f.write(text)

print("Imágenes distribuidas en el manual.")
