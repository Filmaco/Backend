from models.conection import get_connection
from pydantic import BaseModel
from typing import Optional, List
from fastapi import UploadFile, File

# add comenrario

def model_adicionar_comentario(video_id: int, usuario_id: int, conteudo: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO comentarios (video_id, usuario_id, conteudo)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (video_id, usuario_id, conteudo))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Erro ao adicionar comentário:", e)
        return None
    finally:
        cursor.close()
        conn.close()

# listar comentarios
def model_listar_comentarios_por_video(video_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                c.comentario_id,
                c.usuario_id,
                u.nome_completo,
                u.foto_perfil,
                c.video_id,
                c.conteudo,
                c.criado_em,
                c.atualizado_em,
                c.status
            FROM comentarios c
            INNER JOIN usuarios u ON c.usuario_id = u.usuario_id
            WHERE c.video_id = %s
            ORDER BY c.criado_em DESC
        """
        cursor.execute(sql, (video_id,))
        comentarios = cursor.fetchall()
        return comentarios
    except Exception as e:
        print("Erro ao listar comentários:", e)
        return []
    finally:
        cursor.close()
        conn.close()

# excluir
def model_excluir_comentario(comentario_id: int, usuario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            DELETE FROM comentarios 
            WHERE comentario_id = %s AND usuario_id = %s
        """
        cursor.execute(sql, (comentario_id, usuario_id))
        conn.commit()

        return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao excluir comentário:", e)
        return False
    finally:
        cursor.close()
        conn.close()

