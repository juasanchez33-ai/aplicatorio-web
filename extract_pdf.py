import PyPDF2
import os

def extract_pdf(filename, output_name):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return
        
    reader = PyPDF2.PdfReader(filename)
    text = f"=== {filename} ===\n\n"
    for i, page in enumerate(reader.pages):
        text += f"--- Page {i+1} ---\n"
        page_text = page.extract_text()
        text += page_text if page_text else ""
        text += "\n\n"
        
    with open(output_name, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Extracted {filename} to {output_name}")

extract_pdf('Manual_Técnico.pdf', '/tmp/tecnico.txt')
extract_pdf('Manual_Usuario.pdf', '/tmp/usuario.txt')
