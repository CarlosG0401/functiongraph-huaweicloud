# myproject/api.py
import os
import requests

APIG_BASE_URL = os.environ.get("APIG_BASE_URL", "https://a708d8b42e5641628cd7a6ce51e589db.apic.la-south-2.huaweicloudapis.com")

def _url(path: str) -> str:
    # Si en APIG publicaste con prefijo (ej: /v1), inclúyelo aquí.
    return f"{APIG_BASE_URL}{path}"

def get_orders():
    r = requests.get(_url("/orders"), timeout=5)
    r.raise_for_status()
    return r.json()  # Debe ser una lista de dicts: [{oid, fname, lname, price, mail, addr}, ...]

def get_order(oid: int):
    r = requests.get(_url(f"/orders/{oid}"), timeout=5)
    r.raise_for_status()
    return r.json()

def create_order(payload: dict):
    r = requests.post(_url("/orders"), json=payload, timeout=5)
    r.raise_for_status()
    return r.json()

def update_order(oid: int, payload: dict):
    r = requests.put(_url(f"/orders/{oid}"), json=payload, timeout=5)
    r.raise_for_status()
    return r.json()

def delete_order(oid: int):
    r = requests.delete(_url(f"/orders/{oid}"), timeout=5)
    r.raise_for_status()
    return {"ok": True}
