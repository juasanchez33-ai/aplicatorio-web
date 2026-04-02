from fpdf import FPDF

class MyPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="R")

def build_pdf(html_file, output_file):
    pdf = MyPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # fpdf2 write_html usage
    pdf.write_html(html)
    pdf.output(output_file)
    print(f"Built {output_file}")

build_pdf('tecnico.html', 'Manual_Técnico.pdf')
build_pdf('usuario.html', 'Manual_Usuario.pdf')
