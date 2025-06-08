from db_config import conectar

conn = conectar()

if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente LIMIT 5;")
    resultado = cursor.fetchall()
    print("Alguns clientes:")
    for row in resultado:
        print(row)

    cursor.close()
    conn.close()
