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
def model_excluir_avaliacao(avaliacao_id: int, video_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            DELETE FROM avaliacoes 
            WHERE avaliacao_id = %s AND video_id = %s
        """
        cursor.execute(sql, (avaliacao_id, video_id))
        conn.commit()

        return cursor.rowcount > 0
    except Exception as e:
        print("Erro ao excluir avaliacoes:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# ediatr
def model_atualizar_avaliacao(
    avaliacao_id,
    avaliacao=None,
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        campos = []
        valores = []

        if avaliacao:
            campos.append("avaliacao = %s")
            valores.append(avaliacao)
       
        if not campos:
            return False

        campos.append("atualizado_em = CURRENT_TIMESTAMP")
        valores.append(avaliacao_id)

        query = f"""
            UPDATE avaliacoes
            SET {', '.join(campos)}
            WHERE avaliacao_id = %s
        """
        cursor.execute(query, valores)
        conn.commit()
        return True
    
    except Exception as e:
        print("Erro ao atualizar avaliacao:", e)
        return False

    finally:
        cursor.close()
        conn.close()
