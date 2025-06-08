import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            host="10.61.49.170",
            port="5432",
            database="amazon",
            user="misterio_amazon",
            password="amazon123"
        )
        print("Conexão bem-sucedida!")
        return conn
    except Exception as e:
        print("Erro na conexão:", e)
        return None
