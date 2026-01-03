from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from invoice_parser import parse_invoice_xml
from pdf_generator import generate_pdf

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/upload")
async def upload_file(file: UploadFile):
    xml_bytes = await file.read()
    invoice_data = parse_invoice_xml(xml_bytes)

    pdf_path = generate_pdf(invoice_data)

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename="rechnung.pdf"
    )
