from models.conection import get_connection
import logging

logger = logging.getLogger(__name__)

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
