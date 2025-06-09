from models.utils import gerar_hash  
from controllers.validacoes import validar_senha
from models.conection import get_connection
import jwt
from models.utils import verificar_hash
import logging
from models.utils import validar_campos_obrigatorios
from datetime import datetime, timedelta

from models.avaliacao_model import (
   model_adicionar_avaliacao,
   model_excluir_avaliacao,
   model_listar_avaliacaos_por_video,
   model_atualizar_avaliacao,
   model_buscar_ultima_avaliacao_usuario,
   model_listar_ultimas_avaliacoes_por_video,
)

logger = logging.getLogger(__name__)

# add avaliacao

def controller_adicionar_avaliacao(dados):
    campos_obrigatorios = ["video_id", "usuario_id", "avaliacao"]
    validacao = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if validacao["status"] != 200:
        logger.error(f"Falha ao adicionar avaliacao: {validacao['mensagem']}")
        return validacao

    if not dados["avaliacao"].strip():
        logger.error("Falha ao adicionar avaliacao: conteúdo vazio.")
        return {"status": 400, "mensagem": "O conteúdo da avaliação não pode estar vazio."}

    try:
        avaliacao_id = model_adicionar_avaliacao(
            usuario_id=dados["usuario_id"],
            video_id=dados["video_id"],
            avaliacao=dados["avaliacao"]
        )

        if avaliacao_id:
            logger.info(f"Avaliação adicionada com sucesso (ID: {avaliacao_id}).")
            return {
                "status": 200,
                "mensagem": "Avaliação adicionada com sucesso.",
                "data": {
                    "id": avaliacao_id
                }
            }
        else:
            logger.error("Erro ao adicionar Avaliação: retorno nulo do model.")
            return {"status": 500, "mensagem": "Erro ao adicionar avaliação."}
    except Exception as e:
        logger.error(f"Erro inesperado ao adicionar Avaliação: {str(e)}")
        return {"status": 500, "mensagem": str(e)}


# listar avaliacao
def controller_listar_avaliacao(video_id: int):
    try:
        avaliacoes = model_listar_avaliacaos_por_video(video_id)
        return {"status": 200, "dados": avaliacoes}
    except Exception as e:
        logger.error(f"Erro ao listar avaliacoes: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar avaliacoes."}
    

# excluir
def controller_excluir_avaliacao(avaliacao_id: int):
    try:
        sucesso = model_excluir_avaliacao(avaliacao_id,)
        if sucesso:
            logger.info(f"Avaliacao {avaliacao_id} excluído com sucesso.")
            return {"status": 200, "mensagem": "Avaliacao excluído com sucesso."}
        else:
            logger.warning(f"Tentativa de exclusão falhou: avaliacao {avaliacao_id} não encontrado ou usuário sem permissão.")
            return {"status": 404, "mensagem": "Avaliacao não encontrado ou usuário não autorizado."}
    except Exception as e:
        logger.error(f"Erro ao excluir avaliacao: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao excluir avaliacao."}
    
# eidtar
def controller_atualizar_avaliacao(avaliacao_id: int, dados: dict):
    try:
        sucesso = model_atualizar_avaliacao(
            avaliacao_id=avaliacao_id,
            avaliacao=dados.get("avaliacao"),
        )

        if not sucesso:
            return {
                "status": 500,
                "mensagem": "Erro ao atualizar avaliação no banco de dados"
            }

        return {
            "status": 200,
            "mensagem": "Avaliação atualizada com sucesso",
            "id": avaliacao_id
        }

    except Exception as e:
        logger.error(f"Erro ao atualizar avaliacao: {str(e)}")
        return {
            "status": 500,
            "mensagem": "Erro inesperado ao atualizar avaliação"
        }

    
# ultima avalaicao por usuario
def controller_ultima_avaliacao_usuario(usuario_id: int, video_id: int):
    try:
        resultado = model_buscar_ultima_avaliacao_usuario(usuario_id, video_id)
        if resultado:
            return {"status": 200, "dados": resultado}
        else:
            return {"status": 404, "mensagem": "Avaliação não encontrada para este usuário e vídeo."}
    except Exception as e:
        logger.error(f"Erro ao buscar última avaliação do usuário: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao buscar avaliação"}

# ultimas avaliacoes de todos os usuairos por video
def controller_ultimas_avaliacoes_por_video(video_id: int):
    try:
        resultado = model_listar_ultimas_avaliacoes_por_video(video_id)
        return {"status": 200, "dados": resultado}
    except Exception as e:
        logger.error(f"Erro ao buscar últimas avaliações do vídeo: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao buscar avaliações"}