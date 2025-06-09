import psycopg2

DB_CONFIG = {
    'host': '10.61.49.170',
    'port': 5432,
    'dbname': 'amazon',
    'user': 'usuario_crud',
    'password': 'crud123'
}

# === Conecta ao banco ===
def conectar():
    return psycopg2.connect(**DB_CONFIG)