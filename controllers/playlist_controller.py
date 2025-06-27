from fastapi import UploadFile
from models.playlist_model import (
    model_criar_playlist, 
    model_listar_playlists_por_usuario, 
    model_adicionar_video_na_playlist,
    model_listar_videos_da_playlist,
    model_atualizar_playlist,
    model_listar_playlist,
    model_obter_playlist_por_id,
    model_inativar_playlist,
    model_remover_video_da_playlist,
    # model_listar_playlist_usuario
    )
from models.utils import validar_campos_obrigatorios
import os
import shutil
import logging

logger = logging.getLogger(__name__)

# ------------- PLAYLIST ------------

# add playlist
def controller_criar_playlist(dados: dict):
    campos_obrigatorios = ["usuario_id", "titulo"]
    validacao = validar_campos_obrigatorios(dados, campos_obrigatorios)

    if validacao["status"] != 200:
        return validacao

    imagem_nome = dados.get("imagem")
    playlist_id = model_criar_playlist(
        dados["usuario_id"],
        dados["titulo"],
        imagem=imagem_nome
    )

    if playlist_id:
        return {"status": 200, "mensagem": "Playlist criada com sucesso", "id": playlist_id}
    else:
        return {"status": 500, "mensagem": "Erro ao criar playlist"}

# edita playlist
def controller_atualizar_playlist(playlist_id: int, dados: dict):
    try:
        playlist_atualizada = model_atualizar_playlist(
            playlist_id=playlist_id,
            titulo=dados.get("titulo"),
            imagem=dados.get("imagem"),
        )

        if not playlist_atualizada:
            return {"status": 500, "mensagem": "Erro ao atualizar playlist no banco de dados"}

        return {"status": 200, "mensagem": "Playlist atualizada com sucesso", "id": playlist_id}

    except Exception as e:
        logger.error(f"Erro ao atualizar playlist: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao atualizar playlist"}

  
# ------ INATIVA VIDEO------
def controller_inativar_playlist(playlist_id, status):
    try:
        sucesso = model_inativar_playlist(playlist_id, status)
        if sucesso:
            return {"status": 200, "mensagem": "Playlist inativada com sucesso"}
        else:
            return {"status": 400, "mensagem": "Não foi possível inativar a playlist"}
    except Exception as e:
        logger.error(f"Erro ao inativar playlist {playlist_id}: {str(e)}")
        return {"status": 500, "mensagem": "Erro interno ao inativar playlist"}
 
  
    
# lista playlist por usuario
def controller_listar_playlists_por_usuario(usuario_id: int):
    try:
        playlists = model_listar_playlists_por_usuario(usuario_id)
        return {"status": 200, "data": playlists}
    except Exception as e:
        return {"status": 500, "mensagem": "Erro ao listar playlists", "detalhes": str(e)}
    
# pega a playlist por id
def controller_obter_playlist_por_id(playlist_id):
    try:
        playlist = model_obter_playlist_por_id(playlist_id)
        logger.warning(f" Resultado do model: {playlist}")

        if playlist:
            return {"status": 200, "mensagem": "Playlist encontrado com sucesso", "playlist": playlist}
        else:
            logger.warning(f"PLaylist '{playlist}' não encontrado. ------")
            return {"status": 404, "mensagem": "Playlist não encontrado"}

    except Exception as e:
        logger.error(f"Erro ao buscar playlist '{playlist_id}': {str(e)}")
        return {"status": 500, "mensagem": "Erro ao buscar playlist"}

 # ------------- PLAYLIST VIDEO------------

# add video na playlust   
def controller_adicionar_video_na_playlist(dados: dict):
    campos_obrigatorios = ["playlist_id", "video_id"]
    validacao = validar_campos_obrigatorios(dados, campos_obrigatorios)

    if validacao["status"] != 200:
        return validacao

    playlist_video_id = model_adicionar_video_na_playlist(
        dados["playlist_id"],
        dados["video_id"]
    )

    if playlist_video_id:
        return {"status": 200, "mensagem": "Vídeo adicionado à playlist com sucesso", "id": playlist_video_id}
    else:
        return {"status": 500, "mensagem": "Erro ao adicionar vídeo à playlist"}

# lista videos da playlist
def controller_listar_videos_da_playlist(playlist_id: int):
    try:
        videos = model_listar_videos_da_playlist(playlist_id)
        return {"status": 200, "data": videos}
    except Exception as e:
        return {"status": 500, "mensagem": "Erro ao listar vídeos da playlist", "detalhes": str(e)}
    
def controller_listar_playlist():
    try:
        playlists = model_listar_playlist()
        return {"status": 200, "data": playlists}
    except Exception as e:
        return {"status": 500, "mensagem": "Erro ao listar vídeos da playlist", "detalhes": str(e)}


# remover
def controller_remover_video_da_playlist(playlist_id: int, video_id: int):
    try:
        sucesso = model_remover_video_da_playlist(playlist_id, video_id)

        if sucesso:
            return {"status": 200, "mensagem": "Vídeo removido da playlist com sucesso"}
        else:
            return {"status": 404, "mensagem": "Vídeo não encontrado na playlist"}

    except Exception as e:
        return {"status": 500, "mensagem": "Erro ao remover vídeo da playlist", "detalhes": str(e)}
