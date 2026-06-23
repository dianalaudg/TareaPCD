import re
from collections import Counter, defaultdict
from typing import Dict, List, Optional

# ─────────────────────────────────────────────
# PARTE 1: PARSERS DE LOGS
# ─────────────────────────────────────────────

PATRON_HTTP = re.compile(r'''
    ^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})   # IP del cliente
    \s+-\s+-\s+                          # usuario (ignorado)
    \[(?P<timestamp>[^\]]+)\]            # [fecha/hora]
    \s+"(?P<method>[A-Z]+)              # método HTTP
    \s+(?P<path>\S+)                    # ruta
    \s+HTTP/[\d.]+"\s+                  # protocolo
    (?P<status>\d{3})\s+               # código de estado
    (?P<bytes>\d+)\s+                  # bytes
    "(?P<referer>[^"]*)"\s+            # referer
    "(?P<user_agent>[^"]*)"            # user-agent
''', re.VERBOSE)


def parse_http_log(linea: str) -> Optional[Dict]:
    m = PATRON_HTTP.match(linea)
    if not m:
        return None
    return {
        "ip": m.group("ip"),
        "timestamp": m.group("timestamp"),
        "method": m.group("method"),
        "path": m.group("path"),
        "status": int(m.group("status")),
        "bytes": int(m.group("bytes")),
        "referer": m.group("referer"),
        "user_agent": m.group("user_agent"),
    }


PATRON_ERROR = re.compile(r'''
    ^\[(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]  # [timestamp]
    \s+(?P<level>INFO|WARNING|ERROR|CRITICAL|DEBUG)              # nivel
    \s+(?P<module>[\w.]+)                                        # módulo
    \s+-\s+(?P<error_type>\w+):\s+                              # TipoError:
    (?P<message>.+)$                                             # mensaje
''', re.VERBOSE)


def parse_error_log(linea: str) -> Optional[Dict]:
    m = PATRON_ERROR.match(linea)
    if not m:
        return None
    return {
        "timestamp": m.group("timestamp"),
        "level": m.group("level"),
        "module": m.group("module"),
        "error_type": m.group("error_type"),
        "message": m.group("message"),
    }


PATRON_AUTH = re.compile(r'''
    ^\[AUTH\]\s+
    (?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})
    \s+\|\s+user=(?P<user>\S+)
    \s+\|\s+action=(?P<action>\w+)
    \s+\|\s+status=(?P<status>\w+)
    \s+\|\s+ip=(?P<ip>[\d.]+)
    \s+\|\s+(?P<extra_key>\w+)=(?P<extra_val>\S+)
''', re.VERBOSE)


def parse_auth_log(linea: str) -> Optional[Dict]:
    m = PATRON_AUTH.match(linea)
    if not m:
        return None
    extra_key = m.group("extra_key")
    extra_val = m.group("extra_val")
    extra = {extra_key: int(extra_val) if extra_val.isdigit() else extra_val}
    return {
        "timestamp": m.group("timestamp"),
        "user": m.group("user"),
        "action": m.group("action"),
        "status": m.group("status"),
        "ip": m.group("ip"),
        "extra": extra,
    }


PATRON_DB = re.compile(r'''
    ^\[DB-(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]  # timestamp
    \s+(?P<query_type>SLOW_QUERY|QUERY)                             # tipo
    (?:
        \s+executed\s+in\s+(?P<time_normal>[\d.]+)s:              # QUERY normal
        |
        \s+\((?P<time_slow>[\d.]+)s\):                            # SLOW_QUERY
    )
    \s+(?P<query>.+)$                                              # SQL
''', re.VERBOSE)


def parse_db_log(linea: str) -> Optional[Dict]:
    m = PATRON_DB.match(linea)
    if not m:
        return None
    tiempo = m.group("time_normal") or m.group("time_slow")
    return {
        "timestamp": m.group("timestamp"),
        "query_type": m.group("query_type"),
        "execution_time": float(tiempo),
        "query": m.group("query"),
    }


# ─────────────────────────────────────────────
# PARTE 2: ANALIZADOR DE SEGURIDAD
# ─────────────────────────────────────────────

def detectar_ataques_fuerza_bruta(logs_auth: List[Dict]) -> List[Dict]:
    fallos_por_ip = defaultdict(int)
    for log in logs_auth:
        if log.get("status") == "FAILED":
            fallos_por_ip[log["ip"]] += 1
    return [
        {"ip": ip, "intentos": count}
        for ip, count in fallos_por_ip.items()
        if count > 3
    ]


PATRONES_SQL_INJECTION = [
    re.compile(r"(?i)\bOR\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+"),
    re.compile(r"(?i)\bUNION\b.*\bSELECT\b"),
    re.compile(r"--"),
    re.compile(r"(?i)\bDROP\b\s+\bTABLE\b"),
    re.compile(r"(?i)\bDELETE\b\s+\bFROM\b.*\bWHERE\b\s+1\s*=\s*1"),
]


def detectar_sql_injection(logs_db: List[Dict]) -> List[Dict]:
    sospechosos = []
    for log in logs_db:
        query = log.get("query", "")
        for patron in PATRONES_SQL_INJECTION:
            if patron.search(query):
                sospechosos.append(log)
                break
    return sospechosos


PATRON_PATH_TRAVERSAL = re.compile(r'(\.\./|\.\.\\|%2e%2e%2f|%2e%2e/)', re.IGNORECASE)


def detectar_path_traversal(logs_http: List[Dict]) -> List[Dict]:
    return [
        log for log in logs_http
        if PATRON_PATH_TRAVERSAL.search(log.get("path", ""))
    ]


def detectar_errores_criticos(logs_error: List[Dict]) -> List[Dict]:
    criticos = [
        log for log in logs_error
        if log.get("level") in ("ERROR", "CRITICAL")
    ]
    return sorted(criticos, key=lambda x: x["timestamp"])


# ─────────────────────────────────────────────
# PARTE 3: GENERADOR DE REPORTES
# ─────────────────────────────────────────────

def clasificar_linea(linea: str) -> str:
    if PATRON_HTTP.match(linea):
        return "http"
    if PATRON_ERROR.match(linea):
        return "error"
    if linea.startswith("[AUTH]"):
        return "auth"
    if linea.startswith("[DB-"):
        return "db"
    return "desconocido"


def generar_reporte(logs: str) -> Dict:
    lineas = [l for l in logs.splitlines() if l.strip()]

    http_logs, error_logs, auth_logs, db_logs = [], [], [], []
    conteo = {"http": 0, "error": 0, "auth": 0, "db": 0, "desconocido": 0}

    for linea in lineas:
        tipo = clasificar_linea(linea)
        conteo[tipo] += 1
        if tipo == "http":
            r = parse_http_log(linea)
            if r:
                http_logs.append(r)
        elif tipo == "error":
            r = parse_error_log(linea)
            if r:
                error_logs.append(r)
        elif tipo == "auth":
            r = parse_auth_log(linea)
            if r:
                auth_logs.append(r)
        elif tipo == "db":
            r = parse_db_log(linea)
            if r:
                db_logs.append(r)

    # HTTP stats
    por_status = {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}
    rutas = Counter()
    ips = Counter()
    for h in http_logs:
        s = h["status"]
        if 200 <= s < 300:
            por_status["2xx"] += 1
        elif 300 <= s < 400:
            por_status["3xx"] += 1
        elif 400 <= s < 500:
            por_status["4xx"] += 1
        elif 500 <= s < 600:
            por_status["5xx"] += 1
        # Normalizar rutas (quitar query string)
        ruta_base = re.sub(r'\?.*$', '', h["path"])
        rutas[ruta_base] += 1
        ips[h["ip"]] += 1

    # Error stats
    por_nivel = Counter(e["level"] for e in error_logs)
    por_modulo = Counter(e["module"] for e in error_logs)

    # Rendimiento DB
    tiempos = [d["execution_time"] for d in db_logs]
    queries_lentos = [d for d in db_logs if d["query_type"] == "SLOW_QUERY"]
    promedio = sum(tiempos) / len(tiempos) if tiempos else 0.0

    return {
        "resumen": {
            "total_lineas": len(lineas),
            "por_tipo": {k: v for k, v in conteo.items() if k != "desconocido"},
        },
        "http": {
            "total_requests": len(http_logs),
            "por_status": {k: v for k, v in por_status.items() if v > 0},
            "top_rutas": rutas.most_common(5),
            "top_ips": ips.most_common(5),
        },
        "errores": {
            "total": len(error_logs),
            "por_nivel": dict(por_nivel),
            "por_modulo": dict(por_modulo),
        },
        "seguridad": {
            "alertas_fuerza_bruta": detectar_ataques_fuerza_bruta(auth_logs),
            "alertas_sql_injection": detectar_sql_injection(db_logs),
            "alertas_path_traversal": detectar_path_traversal(http_logs),
        },
        "rendimiento": {
            "queries_lentos": queries_lentos,
            "tiempo_promedio_queries": round(promedio, 3),
        },
    }


def mostrar_reporte(reporte: Dict) -> None:
    print("=" * 70)
    print("                    REPORTE DE ANÁLISIS DE LOGS")
    print("=" * 70)

    print("\n📊 RESUMEN GENERAL")
    print("-" * 40)
    print(f"Total de líneas procesadas: {reporte['resumen']['total_lineas']}")
    print("Por tipo:")
    for tipo, count in reporte["resumen"]["por_tipo"].items():
        print(f"  • {tipo.upper()}: {count}")

    if "http" in reporte:
        print("\n🌐 LOGS HTTP")
        print("-" * 40)
        print(f"Total requests: {reporte['http']['total_requests']}")
        print("Por código de estado:")
        for status, count in reporte["http"]["por_status"].items():
            print(f"  • {status}: {count}")
        print("Top 5 rutas más solicitadas:")
        for ruta, count in reporte["http"].get("top_rutas", [])[:5]:
            print(f"  • {ruta}: {count} requests")

    if "errores" in reporte:
        print("\n❌ ERRORES")
        print("-" * 40)
        print(f"Total errores: {reporte['errores']['total']}")
        print("Por nivel:")
        for nivel, count in reporte["errores"]["por_nivel"].items():
            print(f"  • {nivel}: {count}")

    if "seguridad" in reporte:
        print("\n🔒 ALERTAS DE SEGURIDAD")
        print("-" * 40)
        fb = reporte["seguridad"].get("alertas_fuerza_bruta", [])
        if fb:
            print(f"⚠️  Posibles ataques de fuerza bruta: {len(fb)}")
            for alerta in fb:
                print(f"     IP: {alerta['ip']} - {alerta['intentos']} intentos fallidos")
        sql = reporte["seguridad"].get("alertas_sql_injection", [])
        if sql:
            print(f"⚠️  Posibles SQL Injection: {len(sql)}")
            for alerta in sql[:3]:
                print(f"     Query: {alerta['query'][:60]}...")
        pt = reporte["seguridad"].get("alertas_path_traversal", [])
        if pt:
            print(f"⚠️  Posibles Path Traversal: {len(pt)}")
            for alerta in pt[:3]:
                print(f"     Ruta: {alerta['path']}")

    if "rendimiento" in reporte:
        print("\n⏱️  RENDIMIENTO")
        print("-" * 40)
        print(f"Queries lentos detectados: {len(reporte['rendimiento'].get('queries_lentos', []))}")
        if "tiempo_promedio_queries" in reporte["rendimiento"]:
            print(f"Tiempo promedio de queries: {reporte['rendimiento']['tiempo_promedio_queries']:.3f}s")

    print("\n" + "=" * 70)


# ─────────────────────────────────────────────
# BONUS
# ─────────────────────────────────────────────

import json

def exportar_reporte_json(reporte: Dict, archivo: str) -> None:
    reporte_serializable = json.loads(json.dumps(reporte, default=str))
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(reporte_serializable, f, ensure_ascii=False, indent=2)
    print(f"Reporte exportado a {archivo}")


def analisis_temporal(logs_http: List[Dict]) -> Dict:
    horas = Counter()
    for log in logs_http:
        # timestamp formato: 15/Mar/2024:10:23:45 -0600
        m = re.search(r':(\d{2}):\d{2}:\d{2}', log.get("timestamp", ""))
        if m:
            horas[int(m.group(1))] += 1
    return dict(sorted(horas.items()))


BOT_AGENTS = re.compile(
    r'(curl|wget|python-requests|scrapy|bot|spider|crawler|httpx|Go-http-client|PostmanRuntime)',
    re.IGNORECASE
)

def detectar_bots(logs_http: List[Dict]) -> List[Dict]:
    return [
        log for log in logs_http
        if BOT_AGENTS.search(log.get("user_agent", ""))
    ]


# ─────────────────────────────────────────────
# DATOS DE PRUEBA Y EJECUCIÓN
# ─────────────────────────────────────────────

LOGS_PRUEBA = """
192.168.1.100 - - [15/Mar/2024:10:23:45 -0600] "GET /api/users HTTP/1.1" 200 1234 "https://ejemplo.com" "Mozilla/5.0 (Windows NT 10.0)"
192.168.1.101 - - [15/Mar/2024:10:23:46 -0600] "POST /api/login HTTP/1.1" 200 89 "-" "curl/7.68.0"
192.168.1.102 - - [15/Mar/2024:10:23:47 -0600] "GET /admin/../../../etc/passwd HTTP/1.1" 403 0 "-" "sqlmap/1.0"
[2024-03-15 10:24:00] INFO app.startup - Application started successfully on port 8080
[2024-03-15 10:25:12] ERROR app.database - DatabaseConnectionError: Connection refused to host db.server.com:5432
[2024-03-15 10:25:15] WARNING app.cache - CacheWarning: Redis connection timeout, using fallback
[2024-03-15 10:26:00] ERROR app.auth - AuthenticationError: Invalid token for user admin@empresa.com
[AUTH] 2024-03-15 10:30:00 | user=admin@empresa.com | action=LOGIN | status=SUCCESS | ip=10.0.0.5 | session=abc123xyz
[AUTH] 2024-03-15 10:31:00 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=1
[AUTH] 2024-03-15 10:31:30 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=2
[AUTH] 2024-03-15 10:32:00 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=3
[AUTH] 2024-03-15 10:32:30 | user=hacker@mail.com | action=LOGIN | status=FAILED | ip=192.168.1.50 | attempts=4
[AUTH] 2024-03-15 10:33:00 | user=otro@empresa.com | action=LOGOUT | status=SUCCESS | ip=10.0.0.10 | session=def456uvw
[DB-2024-03-15 10:35:22] QUERY executed in 0.045s: SELECT * FROM users WHERE email = 'admin@empresa.com'
[DB-2024-03-15 10:35:25] QUERY executed in 0.012s: SELECT id, name FROM products WHERE active = 1
[DB-2024-03-15 10:36:00] SLOW_QUERY (2.5s): SELECT * FROM orders o JOIN products p ON o.product_id = p.id JOIN users u ON o.user_id = u.id
[DB-2024-03-15 10:37:00] QUERY executed in 0.001s: SELECT * FROM users WHERE username = 'admin' OR 1=1--'
[DB-2024-03-15 10:38:00] QUERY executed in 0.002s: SELECT * FROM users UNION SELECT * FROM passwords
192.168.1.200 - - [15/Mar/2024:10:40:00 -0600] "GET /products?id=1 HTTP/1.1" 200 5678 "https://tienda.com" "Mozilla/5.0"
192.168.1.200 - - [15/Mar/2024:10:40:05 -0600] "GET /products?id=2 HTTP/1.1" 200 4321 "https://tienda.com" "Mozilla/5.0"
192.168.1.201 - - [15/Mar/2024:10:41:00 -0600] "GET /api/users HTTP/1.1" 401 123 "-" "PostmanRuntime/7.26.8"
192.168.1.201 - - [15/Mar/2024:10:41:05 -0600] "GET /api/users HTTP/1.1" 500 0 "-" "PostmanRuntime/7.26.8"
[2024-03-15 10:42:00] ERROR app.api - NullPointerException: Cannot read property 'id' of undefined
[DB-2024-03-15 10:45:00] SLOW_QUERY (5.2s): SELECT COUNT(*) FROM logs WHERE date > '2024-01-01'
""".strip()

if __name__ == "__main__":
    reporte = generar_reporte(LOGS_PRUEBA)
    mostrar_reporte(reporte)