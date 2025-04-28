from models.conection import get_connection

def model_adicionar_video(
    usuario_id,
    nome,
    genero,
    duracao,
    tipo,
    link,
    descricao=None,
    tags=None
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO videos (
            usuario_id, nome, descricao, genero, tags,
            duracao, tipo, link, status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            usuario_id, nome, descricao, genero, tags,
            duracao, tipo, link, 'ativo' 
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


def model_atualizar_video(
    video_id,
    nome=None,
    descricao=None,
    genero=None,
    tags=None,
    duracao=None,
    tipo=None,
    link=None
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
        if tags:
            campos.append("tags = %s")
            valores.append(tags)
        if duracao:
            campos.append("duracao = %s")
            valores.append(duracao)
        if tipo:
            campos.append("tipo = %s")
            valores.append(tipo)
        if link:
            campos.append("link = %s")
            valores.append(link)

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
        
def model_inativar_video(video_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE videos
            SET ativo = 0, atualizado_em = CURRENT_TIMESTAMP
            WHERE video_id = %s
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
        
def model_obter_video_por_id(video_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM videos WHERE video_id = %s", (video_id,))
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

        cursor.execute("SELECT * FROM videos WHERE usuario_id = %s", (usuario_id,))
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

        sql = "SELECT * FROM videos WHERE tipo = %s"
        cursor.execute(sql, (tipo,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao listar vídeos por tipo: {e}")
        return []

    finally:
        cursor.close()
        conn.close()