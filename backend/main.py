from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from invoice_parser import parse_invoice_xml
from pdf_generator import generate_pdf

import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("invoice.html", {"request": request})


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    xml_bytes = await file.read()
    invoice_data = parse_invoice_xml(xml_bytes)
    pdf_path = generate_pdf(invoice_data)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="invoice.pdf"
    )

