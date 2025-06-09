from models.conection import get_connection
import logging

logger = logging.getLogger(__name__)

# estatistica usuario
def model_obter_estatisticas_usuario(usuario_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT COUNT(*) AS total_videos
            FROM videos
            WHERE usuario_id = %s
            AND status = 'ativo'
        """, (usuario_id,))
        total_videos = cursor.fetchone()["total_videos"]

        cursor.execute("""
            SELECT COUNT(*) AS total_seguidos
            FROM seguidores
            WHERE seguidor_id = %s
        """, (usuario_id,))
        total_seguidos = cursor.fetchone()["total_seguidos"]

        cursor.execute("""
            SELECT COUNT(*) AS total_seguidores
            FROM seguidores
            WHERE seguido_id = %s
        """, (usuario_id,))
        total_seguidores = cursor.fetchone()["total_seguidores"]

        return {
            "total_videos": total_videos,
            "total_seguidos": total_seguidos,
            "total_seguidores": total_seguidores
        }

    except Exception as e:
        print(f"Erro ao obter estatísticas do usuário: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

# estatistica seguidores do usuario
def model_listar_seguidores_com_estatisticas(usuario_id: int):
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

        for seguidor in seguidores:
            seguidor_id = seguidor["usuario_id"]

            cursor.execute("""
                SELECT COUNT(*) AS total_videos
                FROM videos
                WHERE usuario_id = %s AND status = 'ativo'
            """, (seguidor_id,))
            seguidor["total_videos"] = cursor.fetchone()["total_videos"]

            cursor.execute("""
                SELECT COUNT(*) AS total_seguidos
                FROM seguidores
                WHERE seguidor_id = %s
            """, (seguidor_id,))
            seguidor["total_seguidos"] = cursor.fetchone()["total_seguidos"]

            cursor.execute("""
                SELECT COUNT(*) AS total_seguidores
                FROM seguidores
                WHERE seguido_id = %s
            """, (seguidor_id,))
            seguidor["total_seguidores"] = cursor.fetchone()["total_seguidores"]

        return seguidores

    except Exception as e:
        raise Exception(f"Erro ao listar seguidores com estatísticas: {str(e)}")
    finally:
        cursor.close()
        conn.close()
   
# estatistica seguidos do usuario     
def model_listar_seguidos_com_estatisticas(usuario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                u.usuario_id, 
                u.nome_completo, 
                u.username, 
                u.foto_perfil,
                (SELECT COUNT(*) FROM videos v WHERE v.usuario_id = u.usuario_id AND v.status = 'ativo') AS total_videos,
                (SELECT COUNT(*) FROM seguidores sg WHERE sg.seguidor_id = u.usuario_id) AS total_seguidos,
                (SELECT COUNT(*) FROM seguidores sr WHERE sr.seguido_id = u.usuario_id) AS total_seguidores
            FROM seguidores s
            JOIN usuarios u ON s.seguido_id = u.usuario_id
            WHERE s.seguidor_id = %s
        """, (usuario_id,))

        return cursor.fetchall()

    except Exception as e:
        raise Exception(f"Erro ao listar seguidos com estatísticas: {str(e)}")
    finally:
        cursor.close()
        conn.close()

