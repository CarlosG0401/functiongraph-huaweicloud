import os, json, pymysql

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "cursorclass": pymysql.cursors.DictCursor,
    "connect_timeout": 5,
}

def get_conn():
    return pymysql.connect(**DB_CONFIG)

def response(status=200, body=None):
    return {
        "statusCode": status,
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",      # habilita CORS (ajústalo si necesitas)
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,Authorization"
        },
        "body": json.dumps(body if body is not None else {})
    }

def parse_body(event):
    try:
        return json.loads(event.get("body") or "{}")
    except Exception:
        return {}

def handler(event, context):
    # event viene de APIG con method, path, queryStringParameters, body, etc.
    method = (event.get("httpMethod") or event.get("method") or "GET").upper()
    path = event.get("path", "/")
    qs = event.get("queryStringParameters") or {}
    body = parse_body(event)

    try:
        if method == "OPTIONS":
            return response(200, {"ok": True})

        if path.endswith("/orders") and method == "GET":
            return list_orders(qs)

        if path.endswith("/orders") and method == "POST":
            return create_order(body)

        # /orders/{oid}
        if path.startswith("/orders/"):
            oid = path.split("/")[-1]
            if not oid.isdigit():
                return response(400, {"error": "oid inválido"})
            oid = int(oid)

            if method == "PUT":
                return update_order(oid, body)
            if method == "DELETE":
                return delete_order(oid)
            if method == "GET":
                return get_order(oid)

        return response(404, {"error": "Ruta no encontrada"})
    except Exception as e:
        # Log en Cloud Eye por defecto
        return response(500, {"error": str(e)})

def list_orders(qs):
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT oid, fname, lname, price, mail, addr FROM order_order ORDER BY oid")
            rows = cur.fetchall()
    return response(200, rows)

def get_order(oid):
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT oid, fname, lname, price, mail, addr FROM order_order WHERE oid=%s", (oid,))
            row = cur.fetchone()
    return response(200, row or {})

def create_order(data):
    required = ["oid","fname","lname","price","mail","addr"]
    if any(k not in data for k in required):
        return response(400, {"error":"Faltan campos", "required": required})
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO order_order (oid, fname, lname, price, mail, addr)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (data["oid"], data["fname"], data["lname"], data["price"], data["mail"], data["addr"]))
        conn.commit()
    return response(201, {"ok": True})

def update_order(oid, data):
    fields = []
    vals = []
    for k in ["fname","lname","price","mail","addr"]:
        if k in data:
            fields.append(f"{k}=%s")
            vals.append(data[k])
    if not fields:
        return response(400, {"error":"Nada que actualizar"})
    vals.append(oid)
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE order_order SET {', '.join(fields)} WHERE oid=%s", vals)
        conn.commit()
    return response(200, {"ok": True})

def delete_order(oid):
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM order_order WHERE oid=%s", (oid,))
        conn.commit()
    return response(200, {"ok": True})
