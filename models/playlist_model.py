from models.conection import get_connection
from pydantic import BaseModel
from typing import Optional, List
from fastapi import UploadFile, File

class PlaylistCreate(BaseModel):
    usuario_id: int
    titulo: str
    imagem: Optional[UploadFile] = File(None)

    class Config:
        orm_mode = True
        

# ------------- PLAYLIST ------------
        
# add playlist
def model_criar_playlist(usuario_id: int, titulo: str, imagem: Optional[str] = None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO playlists (usuario_id, titulo, imagem, status)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (usuario_id, titulo, imagem, 'ativo'))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Erro ao criar playlist:", e)
        return None
    finally:
        cursor.close()
        conn.close()

# edita playlist
def model_atualizar_playlist(
    playlist_id,
    titulo=None,
    imagem=None,
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        campos = []
        valores = []

        if titulo:
            campos.append("titulo = %s")
            valores.append(titulo)
       
        if imagem:
            campos.append("imagem = %s")
            valores.append(imagem)

        if not campos:
            return False

        campos.append("atualizado_em = CURRENT_TIMESTAMP")
        valores.append(playlist_id)

        query = f"""
            UPDATE playlists
            SET {', '.join(campos)}
            WHERE playlist_id = %s
        """
        cursor.execute(query, valores)
        conn.commit()
        return True

    except Exception as e:
        print("Erro ao atualizar playlist:", e)
        return False

    finally:
        cursor.close()
        conn.close()

# listar playlist
def model_listar_playlist():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM playlists")
        playlists = cursor.fetchall()

        return playlists

    except Exception as e:
        print("Erro ao listar playlists:", e)
        return []

    finally:
        cursor.close()
        conn.close()

# Inativar playlist
def model_inativar_playlist(playlist_id, status):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "UPDATE playlists SET status = %s WHERE playlist_id = %s"
        cursor.execute(sql, (status, playlist_id))
        conn.commit()

        print("Playlist inativada com sucesso!", status)
        return True

    except Exception as e:
        print(f"Erro ao inativar playlist: {e} - ", status)
        return False

    finally:
        cursor.close()
        conn.close()
# lista playlist por usuario
def model_listar_playlists_por_usuario(usuario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                p.*, 
                COUNT(pv.video_id) AS total_videos
            FROM playlists p
            LEFT JOIN playlist_videos pv ON p.playlist_id = pv.playlist_id
            WHERE p.usuario_id = %s AND p.status = 'ativo'
            GROUP BY p.playlist_id
            ORDER BY p.criado_em DESC
        """
        cursor.execute(sql, (usuario_id,))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar playlists:", e)
        return []
    finally:
        cursor.close()
        conn.close()

# pega a playlist por id
def model_obter_playlist_por_id(playlist_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        print(f"Buscando usuário ID: {playlist_id}")  
        cursor.execute("SELECT * FROM playlists WHERE playlist_id = %s", (playlist_id,))
        resultado = cursor.fetchone()
        print(f"Resultado da busca: {resultado}")  
        return resultado

    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


        
# ------------- PLAYLIST VIDEO------------

# add video na playlust
def model_adicionar_video_na_playlist(playlist_id: int, video_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO playlist_videos (playlist_id, video_id)
            VALUES (%s, %s)
        """
        cursor.execute(sql, (playlist_id, video_id))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Erro ao adicionar vídeo na playlist:", e)
        return None
    finally:
        cursor.close()
        conn.close()

# lista videos da playlist
def model_listar_videos_da_playlist(playlist_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                v.* 
            FROM videos v
            INNER JOIN playlist_videos pv ON pv.video_id = v.video_id
            WHERE pv.playlist_id = %s
             AND v.status = "ativo"
        """
        cursor.execute(sql, (playlist_id,))
        return cursor.fetchall()
    except Exception as e:
        print("Erro ao listar vídeos da playlist:", e)
        return []
    finally:
        cursor.close()
        conn.close()
        

