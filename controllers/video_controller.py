from models.video_model import (
    VideoCreate,
    model_adicionar_video,
    model_obter_video_por_id,
    model_atualizar_video,
    model_listar_videos_por_usuario,
    model_incrementar_visualizacoes,
    model_listar_videos_por_tipo,
    model_adicionar_tags,
    model_listar_videos_por_tag,
    model_listar_videos_por_genero,
    model_inativar_video,
    model_remover_tags,
    model_obter_nome_tag_por_id
)
import logging
from models.utils import validar_campos_obrigatorios
from models.conection import get_connection
import os
import shutil
from fastapi import File, UploadFile
from typing import Optional, List, Union


logger = logging.getLogger(__name__)

# ------------- CRIA A ATULIZA VIDEO--------------

# criar vidoe
def controller_criar_video(dados: dict):
    campos_obrigatorios = [
        "usuario_id", "nome", "genero", "duracao", "tipo", "link"
    ]
    
    validacao = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if validacao["status"] != 200:
        return validacao

    tipos_validos = ['curta-metragem','longa-metragem','documentário','clipe musical','vlog','anime','serie','gameplay','tutorial','review','reacao','podcast','entrevista','comedia','noticia','educacional','ao vivo','cobertura de evento','animacao','experiencia social','unboxing','viagem','lifestyle','motivacional','parodia']
    
    if dados["tipo"] not in tipos_validos:
        return {"status": 400, "mensagem": "Tipo de vídeo inválido"}

    video_id = model_adicionar_video(
        dados["usuario_id"],
        dados["nome"],
        dados["genero"],
        dados["duracao"],
        dados["tipo"],
        dados["link"],
        descricao=dados.get("descricao"),
        imagem=dados.get("imagem")
    )

    if video_id is None:
        return {"status": 500, "mensagem": "Erro ao salvar vídeo no banco de dados"}
    
    if dados.get("tags"):
        model_adicionar_tags(video_id, dados["tags"].split(","))

    return {"status": 200, "mensagem": "Vídeo criado com sucesso", "id": video_id}

# atualizar video
def controller_atualizar_video(video_id: int, dados: dict):

    tipos_validos = [
        'curta-metragem','longa-metragem','documentário','clipe musical','vlog','anime','serie',
        'gameplay','tutorial','review','reacao','podcast','entrevista','comedia','noticia',
        'educacional','ao vivo','cobertura de evento','animacao','experiencia social','unboxing',
        'viagem','lifestyle','motivacional','parodia'
    ]
    
    if dados.get("tipo") and dados["tipo"] not in tipos_validos:
        return {"status": 400, "mensagem": "Tipo de vídeo inválido"}

    video_atualizado = model_atualizar_video(
        video_id,
        nome=dados.get("nome"),
        descricao=dados.get("descricao"),
        genero=dados.get("genero"),
        duracao=dados.get("duracao"),
        tipo=dados.get("tipo"),
        link=dados.get("link"),
        imagem=dados.get("imagem")
    )

    if not video_atualizado:
        return {"status": 500, "mensagem": "Erro ao atualizar vídeo no banco de dados"}

    tags = dados.get("tags")
    if tags and not isinstance(tags, list):
        tags = [tags]  

    controller_criar_tags(video_id, tags)

    return {"status": 200, "mensagem": "Vídeo atualizado com sucesso", "id": video_id}



# pegar video por id
def controller_obter_video_por_id(video_id):
    try:
        video = model_obter_video_por_id(video_id)
        if video:
            model_incrementar_visualizacoes(video_id)
            return {"status": 200, "data": video}
        else:
            return {"status": 404, "mensagem": "Vídeo não encontrado"}
    except Exception as e:
        logger.error(f"Erro ao buscar vídeo {video_id}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao buscar vídeo"}
   
# criar vizualizacoes e atulziar toda vez que um
# usuario entra na pagina do video
def controller_incrementar_visualizacoes(video_id):
    try:
        sucesso = model_incrementar_visualizacoes(video_id)
        if sucesso:
            return {"status": 200, "mensagem": "Visualizações incrementadas"}
        else:
            return {"status": 400, "mensagem": "Erro ao incrementar visualizações"}
    except Exception as e:
        logger.error(f"Erro ao incrementar visualizações: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao incrementar visualizações"}


# --------------- TAGS ----------------

# cria as tags
def controller_criar_tags(video_id: int, tags_str: str):
    try:
        video = model_obter_video_por_id(video_id)
        if not video:
            return {"status": 400, "mensagem": "Vídeo não encontrado"}

        if not tags_str:
            return {"status": 400, "mensagem": "Nenhuma tag fornecida"}

        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

        if not tags:
            return {"status": 400, "mensagem": "Tags inválidas"}

        sucesso = model_adicionar_tags(video_id, tags)

        if sucesso:
            return {"status": 200, "mensagem": "Tags adicionadas com sucesso"}
        else:
            return {"status": 500, "mensagem": "Erro ao adicionar tags"}

    except Exception as e:
        logger.error(f"Erro ao criar tags para o vídeo {video_id}: {str(e)}")
        return {"status": 500, "mensagem": "Erro interno ao adicionar tags"}

# pesquiasar tag por id
def controller_obter_nome_tag_por_id(id_tag: int):
    try:
        nome_tag = model_obter_nome_tag_por_id(id_tag)
        if nome_tag:
            return {"status": 200, "data": nome_tag}
        else:
            return {"status": 404, "mensagem": "Tag não encontrada"}
    except Exception as e:
        logger.error(f"Erro ao buscar tag {id_tag}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao buscar nome da tag"}

 
 # INATIVA VIDEO


# atualizar tags ( ----  com defeito -----)
def controller_atualizar_tags(video_id: int, tags: Optional[Union[str, List[str]]]):
    if not tags:
        return
    
    if isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    if not isinstance(tags, list):
        return

    for tag in tags:
        model_adicionar_tags(video_id, tag)


# ------ INATIVA VIDEO------
def controller_inativar_video(video_id: int):
    try:
        sucesso = model_inativar_video(video_id)
        if sucesso:
            return {"status": 200, "mensagem": "Vídeo inativado com sucesso"}
        else:
            return {"status": 400, "mensagem": "Não foi possível inativar o vídeo"}
    except Exception as e:
        logger.error(f"Erro ao inativar vídeo {video_id}: {str(e)}")
        return {"status": 500, "mensagem": "Erro interno ao inativar vídeo"}
 

 
# ----------------- LISTAR -----------

# listar tudo
def controller_listar_videos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
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
        """)
        videos = cursor.fetchall()

        return {"status": 200, "data": videos}

    except Exception as e:
        logger.error(f"Erro ao listar vídeos: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar vídeos"}

    finally:
        cursor.close()
        conn.close()

# listar por tipo
def controller_listar_videos_por_tipo(tipo):
    try:
        videos = model_listar_videos_por_tipo(tipo)
        return {"status": 200, "data": videos}
    except Exception as e:
        logger.error(f"Erro ao listar vídeos do tipo {tipo}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar vídeos"}
 
# listar por genro
def controller_listar_videos_por_genero(genero):
    try:
        videos = model_listar_videos_por_genero(genero)
        return {"status": 200, "data": videos}
    except Exception as e:
        logger.error(f"Erro ao listar vídeos do gênero {genero}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar vídeos"}
   
# listar por usuario
def controller_listar_videos_por_usuario(usuario_id):
    try:
        videos = model_listar_videos_por_usuario(usuario_id)
        return {"status": 200, "data": videos}
    except Exception as e:
        logger.error(f"Erro ao listar vídeos do usuário {usuario_id}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar vídeos"}
 
# listar por tag  
def controller_listar_videos_por_tag(nome_tag: str):
    try:
        videos = model_listar_videos_por_tag(nome_tag)
        if videos:
            return {"status": 200, "data": videos}
        else:
            return {"status": 404, "mensagem": "Nenhum vídeo encontrado com essa tag"}
    except Exception as e:
        logger.error(f"Erro ao listar vídeos por tag '{nome_tag}': {str(e)}")
        return {"status": 500, "mensagem": "Erro ao buscar vídeos por tag"}  

# listar as tags
def controller_listar_tags():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM tags_videos")
        tags = cursor.fetchall()

        return {"status": 200, "data": tags}
    except Exception as e:
        logger.error(f"Erro ao listar tags: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar tags"}
    
   
    
    
    
    
    
    
    
    
    
    
    
    