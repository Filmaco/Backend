from models.conection import get_connection
from pydantic import BaseModel
from typing import Optional
from fastapi import File, UploadFile
from typing import List

class VideoCreate(BaseModel):
    usuario_id: int
    nome: str
    genero: str
    duracao: str
    tipo: str
    link: str
    descricao: Optional[str] = None
    tags: Optional[str] = None
    imagem: Optional[UploadFile] = File(None)  

    class Config:
        orm_mode = True

class TagCreate(BaseModel):
    video_id: int
    nome_tag: str

# add video
def model_adicionar_video(
    usuario_id,
    nome,
    genero,
    duracao,
    tipo,
    link,
    descricao=None,
    imagem=None
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO videos (
            usuario_id, nome, descricao, genero, duracao, tipo, link, imagem, status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            usuario_id, nome, descricao, genero, duracao, tipo, link, imagem, 'ativo'
        )

        cursor.execute(sql, valores)
        conn.commit()
        return cursor.lastrowid 

    except Exception as e:
        print("Erro ao adicionar vídeo:", e)
        return None

    finally:
        cursor.close()
        conn.close()



# atualizar video
def model_atualizar_video(
    video_id,
    nome=None,
    descricao=None,
    genero=None,
    duracao=None,
    tipo=None,
    link=None,
    imagem=None
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        campos = []
        valores = []

        if nome:
            campos.append("nome = %s")
            valores.append(nome)
        if descricao:
            campos.append("descricao = %s")
            valores.append(descricao)
        if genero:
            campos.append("genero = %s")
            valores.append(genero)
        if duracao:
            campos.append("duracao = %s")
            valores.append(duracao)
        if tipo:
            campos.append("tipo = %s")
            valores.append(tipo)
        if link:
            campos.append("link = %s")
            valores.append(link)
            
        if imagem:
            campos.append("imagem = %s")
            valores.append(imagem)

        if not campos:
            return False

        campos.append("atualizado_em = CURRENT_TIMESTAMP")
        valores.append(video_id)

        query = f"""
            UPDATE videos
            SET {', '.join(campos)}
            WHERE video_id = %s
        """
        cursor.execute(query, valores)
        conn.commit()
        return True

    except Exception as e:
        print("Erro ao atualizar vídeo:", e)
        return False

    finally:
        cursor.close()
        conn.close()
        
# inativar video
def model_inativar_video(video_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE videos SET status = 'inativo' WHERE video_id = %s
        """
        cursor.execute(sql, (video_id,))
        conn.commit()
        return True

    except Exception as e:
        print(f"Erro ao inativar vídeo: {e}")
        return False

    finally:
        cursor.close()
        conn.close()
        
# def model_inativar_video(video_id, status):
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()

#         sql = """
#             "UPDATE videos SET status = %s WHERE video_id = %s"
#         """
#         cursor.execute(sql, (status, video_id,))
#         conn.commit()
#         return True

#     except Exception as e:
#         print(f"Erro ao inativar vídeo: {e}")
#         return False

#     finally:
#         cursor.close()
#         conn.close()
        
def model_obter_video_por_id(video_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
                       SELECT 
                            v.*, 
                            u.usuario_id, 
                            u.nome_completo AS nome_usuario, 
                            GROUP_CONCAT(t.nome_tag) AS tags
                        FROM 
                            videos v
                        LEFT JOIN 
                            tags_videos t ON v.video_id = t.video_id
                        JOIN 
                            usuarios u ON v.usuario_id = u.usuario_id
                        WHERE 
                            v.status = 'ativo' 
                            AND v.video_id = %s
                        GROUP BY 
                            v.video_id, u.usuario_id 
                       """, (video_id,))
        return cursor.fetchone()

    except Exception as e:
        print(f"Erro ao buscar vídeo: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

def model_listar_videos_por_usuario(usuario_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM videos WHERE usuario_id = %s ", (usuario_id,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao listar vídeos do usuário: {e}")
        return []

    finally:
        cursor.close()
        conn.close()
  
# listar videos por usuairo apenas ativos      
def model_listar_videos_ativos_por_usuario(usuario_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM videos WHERE usuario_id = %s AND status = 'ativo'", (usuario_id,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao listar vídeos do usuário: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

def model_incrementar_visualizacoes(video_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "UPDATE videos SET visualizacoes = visualizacoes + 1 WHERE video_id = %s"
        cursor.execute(sql, (video_id,))
        conn.commit()
        return True

    except Exception as e:
        print(f"Erro ao incrementar visualizações: {e}")
        return False

    finally:
        cursor.close()
        conn.close()

def model_listar_videos_por_tipo(tipo):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM videos WHERE tipo = %s ORDER BY v.criado_em DESC"
        cursor.execute(sql, (tipo,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao listar vídeos por tipo: {e}")
        return []

    finally:
        cursor.close()
        conn.close()
        
def model_listar_videos_por_genero(genero):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
                SELECT 
                    v.*, 
                    u.usuario_id,
                    u.nome_completo AS nome_usuario,
                    GROUP_CONCAT(t.nome_tag) AS tags
                FROM videos v
                JOIN usuarios u ON v.usuario_id = u.usuario_id
                LEFT JOIN tags_videos t ON v.video_id = t.video_id
                WHERE v.genero = %s AND v.status = 'ativo'
                GROUP BY v.video_id
                ORDER BY v.criado_em DESC
            """
        cursor.execute(sql, (genero,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao listar vídeos por gênero: {e}")
        return []

    finally:
        cursor.close()
        conn.close()
             
def model_adicionar_tags(video_id: int, tags: List[str]):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO tags_videos (video_id, nome_tag) VALUES (%s, %s)"
        valores = [(video_id, tag.strip()) for tag in tags if tag.strip()]

        cursor.executemany(sql, valores)
        conn.commit()
        return True

    except Exception as e:
        print("Erro ao adicionar tags:", e)
        return False

    finally:
        cursor.close()
        conn.close()
   
def model_remover_tags(video_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM tags_videos WHERE video_id = %s"
        cursor.execute(query, (video_id,))
        conn.commit()
    except Exception as e:
        print("Erro ao remover tags:", e)
    finally:
        cursor.close()
        conn.close()   
        
def model_listar_videos_por_tag(nome_tag: Optional[str]):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if nome_tag and nome_tag.lower() != 'null':
            query = """
                SELECT 
                    v.*, 
                    u.usuario_id,
                    u.nome_completo AS nome_usuario,
                    GROUP_CONCAT(t.nome_tag) AS tags
                FROM videos v
                JOIN tags_videos t ON v.video_id = t.video_id
                JOIN usuarios u ON v.usuario_id = u.usuario_id
                WHERE t.nome_tag = %s AND v.status = 'ativo'
                GROUP BY v.video_id
                ORDER BY v.criado_em DESC
            """
            cursor.execute(query, (nome_tag,))
        else:
            query = """
                  SELECT 
                    v.*, 
                    u.usuario_id,
                    u.nome_completo AS nome_usuario,
                    GROUP_CONCAT(t.nome_tag) AS tags
                FROM videos v
                LEFT JOIN tags_videos t ON v.video_id = t.video_id
                JOIN usuarios u ON v.usuario_id = u.usuario_id
                WHERE v.status = 'ativo'
                GROUP BY v.video_id
            """
            cursor.execute(query)

        resultados = cursor.fetchall()

        for video in resultados:
            if video.get("tags"):
                video["tags"] = [tag.strip() for tag in video["tags"].split(",")]
            else:
                video["tags"] = []
        return resultados

    except Exception as e:
        print(f"Erro ao buscar vídeos pela tag '{nome_tag}': {e}")
        return []

    finally:
        cursor.close()
        conn.close()


# -------------- TAGS --------------

# pesquisar tag por id
def model_obter_nome_tag_por_id(id_tag: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT nome_tag FROM tags_videos WHERE id_tag = %s"
        cursor.execute(query, (id_tag,))
        resultado = cursor.fetchone()

        if resultado:
            return resultado["nome_tag"]
        return None

    except Exception as e:
        print(f"Erro ao obter nome da tag pelo ID: {e}")
        return None

    finally:
        cursor.close()
        conn.close()











        


        