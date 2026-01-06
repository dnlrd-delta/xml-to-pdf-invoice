import xml.etree.ElementTree as ET
from typing import Dict, Any, List

# -----------------------------
# Hilfsfunktionen
# -----------------------------

def find_text(root, paths, default="") -> str:
    """Versucht mehrere XPath-Pfade und gibt den ersten gefundenen Text zurück."""
    for path in paths:
        el = root.find(path)
        if el is not None and el.text:
            return el.text.strip()
    return default


def to_float(value, default=0.0) -> float:
    try:
        return float(value.replace(",", "."))
    except Exception:
        return default


# -----------------------------
# Hauptparser (E1–E6)
# -----------------------------

def parse_invoice_xml(xml_bytes: bytes) -> Dict[str, Any]:
    # E1 – XML lesen
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        raise ValueError(f"Ungültiges XML: {e}")

    # E2/E3 – Meta-Daten
    invoice_number = find_text(root, [
        ".//InvoiceNumber",
        ".//ID",
        ".//DocumentNumber"
    ])

    invoice_date = find_text(root, [
        ".//InvoiceDate",
        ".//IssueDate",
        ".//Date"
    ])

    due_date = find_text(root, [
        ".//DueDate",
        ".//PaymentDueDate"
    ])

    # E4 – Positionen
    items: List[Dict[str, Any]] = []

    for i, item in enumerate(root.findall(".//Item"), start=1):
        qty = to_float(find_text(item, [".//Quantity"], "1"), 1)
        unit = to_float(find_text(item, [".//UnitPrice", ".//Price"], "0"), 0)

        items.append({
            "position": i,
            "description": find_text(item, [".//Description", ".//Name"], ""),
            "quantity": qty,
            "unit_price": unit,
            "total": round(qty * unit, 2)
        })

    # Fallback: keine Items gefunden
    if not items:
        items.append({
            "position": 1,
            "description": "Leistung",
            "quantity": 1,
            "unit_price": 0.0,
            "total": 0.0
        })

    # E5 – Summen
    net_calc = sum(i["total"] for i in items)

    net = to_float(find_text(root, [".//NetAmount"], str(net_calc)), net_calc)
    tax = to_float(find_text(root, [".//TaxAmount"], "0"), 0)
    gross = to_float(find_text(root, [".//TotalAmount"], str(net + tax)), net + tax)

    # E6 – Einheitliche Struktur
    invoice: Dict[str, Any] = {
        "supplier": {
            "name": find_text(root, [".//Supplier//Name", ".//Seller//Name"], ""),
            "street": find_text(root, [".//Supplier//Street"], ""),
            "zip": find_text(root, [".//Supplier//PostalCode"], ""),
            "city": find_text(root, [".//Supplier//City"], ""),
            "country": find_text(root, [".//Supplier//Country"], ""),
            "vat_id": find_text(root, [".//Supplier//VATID"], "")
        },
        "customer": {
            "name": find_text(root, [".//Customer//Name", ".//Buyer//Name"], ""),
            "street": find_text(root, [".//Customer//Street"], ""),
            "zip": find_text(root, [".//Customer//PostalCode"], ""),
            "city": find_text(root, [".//Customer//City"], ""),
            "country": find_text(root, [".//Customer//Country"], "")
        },
        "meta": {
            "invoice_number": invoice_number,
            "invoice_date": invoice_date,
            "due_date": due_date
        },
        "items": items,
        "totals": {
            "net": round(net, 2),
            "tax": round(tax, 2),
            "gross": round(gross, 2)
        }
    }

    return invoice

