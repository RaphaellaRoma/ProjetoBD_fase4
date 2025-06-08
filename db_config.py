import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            host="10.61.49.170",       # IP do servidor (verifique se está certo)
            port="5432",               # Porta padrão do PostgreSQL
            database="amazon",         # Nome do seu banco
            user="misterio_amazon",           # Usuário
            password="amazon123"  # Coloque sua senha real
        )
        print("Conexão bem-sucedida!")
        return conn
    except Exception as e:
        print("Erro na conexão:", e)
        return None
