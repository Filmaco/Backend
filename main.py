from models.conection import get_connection

def teste():
    try:
        conn = get_connection()
        if conn.is_connected():
            print("banco conectado")
        conn.close()
    except Exception as e:
        print("erro ao conectar ", e)

if __name__ == "__main__":
    teste()