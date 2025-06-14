from datetime import datetime, timedelta
import logging
from models.denuncia_model import (
    model_denunciar_conteudo,
    model_listar_denuncias,
    model_atualizar_status_denuncia,
    model_remover_video,
    model_remover_comentario,
    model_obter_denuncia_por_id,
)
from models.utils import validar_campos_obrigatorios

logger = logging.getLogger(__name__)

# adiciona denuncia
def controller_denunciar_conteudo(dados):
    try:
        campos_obrigatorios = ['usuario_id', 'motivo']
        validacao = validar_campos_obrigatorios(dados, campos_obrigatorios)

        if validacao["status"] != 200:
            return {
                "status": 400,
                "mensagem": validacao["mensagem"]
            }

        resposta = model_denunciar_conteudo(
            usuario_id=dados["usuario_id"],
            motivo=dados["motivo"],
            video_id=dados.get("video_id"),
        )

        return {
            "status": 201,
            "mensagem": resposta["mensagem"]
        }

    except Exception as e:
        logger.error(f"Erro ao denunciar conteúdo: {str(e)}")
        return {
            "status": 500,
            "mensagem": "Erro interno ao registrar denúncia"
        }


# lista denuncia      
def controller_listar_denuncias():
    try:
        denuncias = model_listar_denuncias()

        return {
            "status": 200,
            "mensagem": "Denúncias listadas com sucesso",
            "denuncias": denuncias
        }

    except Exception as e:
        logger.error(f"Erro ao listar denúncias: {str(e)}")
        return {
            "status": 500,
            "mensagem": "Erro interno ao listar denúncias"
        }

 
# atualiza denuncia       
def controller_atualizar_status_denuncia(denuncia_id, novo_status):
    try:
        if novo_status not in ['pendente', 'resolvido', 'impedimento']:
            return {
                "status": 400,
                "mensagem": "Status inválido. Use 'pendente', 'resolvido' ou 'impedimento'"
            }

        resposta = model_atualizar_status_denuncia(denuncia_id, novo_status)

        return {
            "status": 200,
            "mensagem": resposta["mensagem"]
        }

    except Exception as e:
        logger.error(f"Erro ao atualizar status da denúncia {denuncia_id}: {str(e)}")
        return {
            "status": 500,
            "mensagem": "Erro interno ao atualizar status da denúncia"
        }

# exclui denuncia
def controller_remover_conteudo_denunciado(denuncia):
    try:
        video_id = denuncia.get("video_id")
        comentario_id = denuncia.get("comentario_id")

        if video_id:
            resposta = model_remover_video(video_id)
            return {
                "status": 200,
                "mensagem": f"Vídeo {video_id} removido com sucesso"
            }

        elif comentario_id:
            resposta = model_remover_comentario(comentario_id)
            return {
                "status": 200,
                "mensagem": f"Comentário {comentario_id} removido com sucesso"
            }

        else:
            return {
                "status": 400,
                "mensagem": "Nenhum vídeo ou comentário associado à denúncia"
            }

    except Exception as e:
        logger.error(f"Erro ao remover conteúdo denunciado: {str(e)}")
        return {
            "status": 500,
            "mensagem": "Erro interno ao remover conteúdo denunciado"
        }
        
# obter por id
def controller_obter_denuncia_por_id(denuncia_id: int):
    try:
        denuncia = model_obter_denuncia_por_id(denuncia_id)

        if denuncia:
            return {
                "status": 200,
                "mensagem": "Denúncia encontrada com sucesso",
                "denuncia": denuncia
            }
        else:
            return {
                "status": 404,
                "mensagem": "Denúncia não encontrada"
            }

    except Exception as e:
        logger.error(f"Erro ao obter denúncia por ID {denuncia_id}: {str(e)}")
        return {
            "status": 500,
            "mensagem": "Erro interno ao buscar denúncia"
        }
