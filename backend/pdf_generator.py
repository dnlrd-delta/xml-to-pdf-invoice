from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import uuid

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def generate_pdf(invoice):
    os.makedirs("pdfs", exist_ok=True)

    filename = f"{uuid.uuid4()}.pdf"
    output_path = os.path.abspath(os.path.join("pdfs", filename))

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setFont("Helvetica", 12)

    y = 800
    c.drawString(50, y, "RECHNUNG")
    y -= 40

    c.drawString(50, y, f"Rechnungsnummer: {invoice.get('number', '')}")
    y -= 20
    c.drawString(50, y, f"Datum: {invoice.get('date', '')}")
    y -= 20
    c.drawString(50, y, f"Kunde: {invoice.get('customer', '')}")

    c.showPage()
    c.save()

 # Template laden
    template = env.get_template('invoice.html')

    # Standardwerte für fehlende Felder
    context = {
        'seller': invoice_data.get('seller', {}),
        'buyer': invoice_data.get('buyer', {}),
        'items': invoice_data.get('items', []),
        'invoice_number': invoice_data.get('invoice_number', ''),
        'date': invoice_data.get('date', ''),
        'total': invoice_data.get('total', 0.0)
    }
# HTML rendern
    html_out = template.render(context)

    # PDF erstellen
    pdf = weasyprint.HTML(string=html_out).write_pdf()

    # Sicherstellen, dass Zielordner existiert
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # PDF speichern
    with open(output_path, 'wb') as f:
        f.write(pdf)

    return output_path



