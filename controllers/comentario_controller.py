from models.utils import gerar_hash  
from controllers.validacoes import validar_senha
from models.conection import get_connection
import jwt
from models.utils import verificar_hash
import logging
from models.utils import validar_campos_obrigatorios
from datetime import datetime, timedelta

from models.comentario_modal import (
    model_adicionar_comentario,
    model_listar_comentarios_por_video,
    model_excluir_comentario
)

logger = logging.getLogger(__name__)

# add comentario

def controller_adicionar_comentario(dados):
    campos_obrigatorios = ["video_id", "usuario_id", "conteudo"]
    validacao = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if validacao["status"] != 200:
        logger.error(f"Falha ao adicionar comentário: {validacao['mensagem']}")
        return validacao

    if not dados["conteudo"].strip():
        logger.error("Falha ao adicionar comentário: conteúdo vazio.")
        return {"status": 400, "mensagem": "O conteúdo do comentário não pode estar vazio."}

    try:
        comentario_id = model_adicionar_comentario(
            video_id=dados["video_id"],
            usuario_id=dados["usuario_id"],
            conteudo=dados["conteudo"]
        )
        if comentario_id:
            logger.info(f"Comentário adicionado com sucesso (ID: {comentario_id}).")
            return {"status": 200, "mensagem": "Comentário adicionado com sucesso."}
        else:
            logger.error("Erro ao adicionar comentário: retorno nulo do model.")
            return {"status": 500, "mensagem": "Erro ao adicionar comentário."}
    except Exception as e:
        logger.error(f"Erro inesperado ao adicionar comentário: {str(e)}")
        return {"status": 500, "mensagem": str(e)}

# listar comentario

def controller_listar_comentarios_por_video(video_id: int):
    try:
        comentarios = model_listar_comentarios_por_video(video_id)
        return {"status": 200, "dados": comentarios}
    except Exception as e:
        logger.error(f"Erro ao listar comentários: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar comentários."}
    
# excluir
def controller_excluir_comentario(comentario_id: int, usuario_id: int):
    try:
        sucesso = model_excluir_comentario(comentario_id, usuario_id)
        if sucesso:
            logger.info(f"Comentário {comentario_id} excluído com sucesso.")
            return {"status": 200, "mensagem": "Comentário excluído com sucesso."}
        else:
            logger.warning(f"Tentativa de exclusão falhou: comentário {comentario_id} não encontrado ou usuário sem permissão.")
            return {"status": 404, "mensagem": "Comentário não encontrado ou usuário não autorizado."}
    except Exception as e:
        logger.error(f"Erro ao excluir comentário: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao excluir comentário."}