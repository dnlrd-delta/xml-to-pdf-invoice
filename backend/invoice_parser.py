import xml.etree.ElementTree as ET

def parse_invoice_xml(xml_bytes: bytes) -> dict:
    root = ET.fromstring(xml_bytes)

    invoice = {
        "number": root.findtext("number", "-"),
        "date": root.findtext("date", "-"),
        "customer": {
            "name": root.findtext("customer/name", "-"),
            "address": root.findtext("customer/address", "-"),
        },
        "items": []
    }

    for item in root.findall("items/item"):
        invoice["items"].append({
            "description": item.findtext("description", "-"),
            "quantity": int(item.findtext("quantity", "0")),
            "price": float(item.findtext("price", "0"))
        })

    return invoice
