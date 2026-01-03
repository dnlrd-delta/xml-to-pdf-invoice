from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import uuid

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

    return output_path



