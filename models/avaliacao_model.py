from models.conection import get_connection
from pydantic import BaseModel
from typing import Optional, List
from fastapi import UploadFile, File

# add comenrario
def model_adicionar_avaliacao(usuario_id: int, video_id: int, avaliacao: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO avaliacoes (usuario_id, video_id, avaliacao)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (usuario_id, video_id, avaliacao))
    avaliacao_id = cursor.lastrowid  

    conn.commit()
    cursor.close()
    conn.close()

    return avaliacao_id


# listar avaliacaos
def model_listar_avaliacaos_por_video(video_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT COUNT(*) AS total_nao_gostei
            FROM avaliacoes
            WHERE video_id = %s
            AND avaliacao = '1'
        """, (video_id,))
        total_nao_gostei = cursor.fetchone()["total_nao_gostei"] 
        
        cursor.execute("""
            SELECT COUNT(*) AS total_gostei
            FROM avaliacoes
            WHERE video_id = %s
            AND avaliacao = '2'
        """, (video_id,))
        total_gostei = cursor.fetchone()["total_gostei"]  
        
        cursor.execute("""
            SELECT COUNT(*) AS total_gostei_muito
            FROM avaliacoes
            WHERE video_id = %s
            AND avaliacao = '3'
        """, (video_id,))
        total_gostei_muito = cursor.fetchone()["total_gostei_muito"]   
        
        return {
            "total_nao_gostei": total_nao_gostei,
            "total_gostei": total_gostei,
            "total_gostei_muito": total_gostei_muito
        }

    except Exception as e:
        print(f"Erro ao obter total de avalaicoes do usuário: {e}")
        return None

# excluir
def model_excluir_avaliacao(avaliacao_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            DELETE FROM avaliacoes 
            WHERE avaliacao_id = %s
        """
        cursor.execute(sql, (avaliacao_id,))
        conn.commit()

        return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao excluir avaliacoes:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# editar
def model_atualizar_avaliacao(avaliacao_id, avaliacao=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if avaliacao is None:
            return False  # Nada a atualizar

        query = """
            UPDATE avaliacoes
            SET avaliacao = %s,
                atualizado_em = CURRENT_TIMESTAMP
            WHERE avaliacao_id = %s
        """
        valores = (avaliacao, avaliacao_id)
        cursor.execute(query, valores)
        conn.commit()
        return True

    except Exception as e:
        print("Erro ao atualizar avaliacao:", e)
        return False

    finally:
        cursor.close()
        conn.close()



# ultima avaliacao por usuario
def model_buscar_ultima_avaliacao_usuario(usuario_id: int, video_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM avaliacoes
            WHERE usuario_id = %s AND video_id = %s
            ORDER BY avaliacao_id DESC
            LIMIT 1
        """, (usuario_id, video_id,))

        resultado = cursor.fetchone()
        return resultado

    except Exception as e:
        print("Erro ao buscar última avaliação:", e)
        return None
    finally:
        cursor.close()
        conn.close()

# lista de ultimas avaliacoes de todos os usuarios por video
def model_listar_ultimas_avaliacoes_por_video(video_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT COUNT(*) AS total_dislike
            FROM avaliacoes
            WHERE video_id = %s AND avaliacao = '1'
        """, (video_id,))
        total_dislike = cursor.fetchone()["total_dislike"]

        cursor.execute("""
            SELECT COUNT(*) AS total_like
            FROM avaliacoes
            WHERE video_id = %s AND avaliacao = '2'
        """, (video_id,))
        total_like = cursor.fetchone()["total_like"]

        cursor.execute("""
            SELECT COUNT(*) AS total_love
            FROM avaliacoes
            WHERE video_id = %s AND avaliacao = '3'
        """, (video_id,))
        total_love = cursor.fetchone()["total_love"]

        return {
            "total_dislike": total_dislike,
            "total_like": total_like,
            "total_love": total_love,
        }

    except Exception as e:
        print(f"Erro ao obter estatísticas de avaliações: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

