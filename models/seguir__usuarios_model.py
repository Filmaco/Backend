from models.conection import get_connection

#seguir
def model_seguir_usuario(seguidor_id: int, seguido_id: int):
    try:
        if seguidor_id == seguido_id:
            raise Exception("Usuário não pode seguir a si mesmo.")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM seguidores WHERE seguidor_id = %s AND seguido_id = %s
        """, (seguidor_id, seguido_id))

        if cursor.fetchone():
            raise Exception("Usuário já está seguindo.")

        cursor.execute("""
            INSERT INTO seguidores (seguidor_id, seguido_id) VALUES (%s, %s)
        """, (seguidor_id, seguido_id))

        conn.commit()
    except Exception as e:
        raise Exception(f"Erro ao seguir usuário: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def model_ja_segue(seguidor_id: int, seguido_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM seguidores WHERE seguidor_id = %s AND seguido_id = %s
    """, (seguidor_id, seguido_id))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return bool(resultado)

# deixar se deguir
def model_deixar_de_seguir(seguidor_id: int, seguido_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM seguidores WHERE seguidor_id = %s AND seguido_id = %s
        """, (seguidor_id, seguido_id))

        if cursor.rowcount == 0:
            raise Exception("Você não está seguindo este usuário.")

        conn.commit()
    except Exception as e:
        raise Exception(f"Erro ao deixar de seguir usuário: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# lista de seguidores
def model_listar_seguidores(usuario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT u.usuario_id, u.nome_completo, u.username, u.foto_perfil
            FROM seguidores s
            JOIN usuarios u ON s.seguidor_id = u.usuario_id
            WHERE s.seguido_id = %s
        """, (usuario_id,))  

        seguidores = cursor.fetchall()

        return seguidores

    except Exception as e:
        raise Exception(f"Erro ao listar seguidores: {str(e)}")
    finally:
        cursor.close()
        conn.close()
