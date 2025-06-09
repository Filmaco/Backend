from models.estatistica_model import (
    model_obter_estatisticas_usuario,
    model_listar_seguidores_com_estatisticas,
    model_listar_seguidos_com_estatisticas,
    )
from models.utils import gerar_hash  
from controllers.validacoes import validar_senha
from models.conection import get_connection
import jwt
from models.utils import verificar_hash
import logging
from models.utils import validar_campos_obrigatorios
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def controller_obter_estatisticas_usuario(usuario_id):
    try:
        estatisticas = model_obter_estatisticas_usuario(usuario_id)
        
        if estatisticas is not None:
            return {
                "status": 200,
                "mensagem": "Estatísticas do usuário obtidas com sucesso",
                "estatisticas": estatisticas
            }
        else:
            return {
                "status": 404,
                "mensagem": "Usuário não encontrado ou erro ao obter estatísticas"
            }
    
    except Exception as e:
        logger.error(f"Erro no controller ao obter estatísticas do usuário {usuario_id}: {str(e)}")
        return {
            "status": 500,
            "mensagem": "Erro interno ao obter estatísticas do usuário"
        }
        
def controller_listar_seguidores_com_estatisticas(usuario_id: int):
    try:
        seguidores = model_listar_seguidores_com_estatisticas(usuario_id)

        return {
            "status": 200,
            "mensagem": "Seguidores listados com sucesso",
            "seguidores": seguidores
        }

    except Exception as e:
        logger.error(f"Erro ao listar seguidores com estatísticas para o usuário {usuario_id}: {str(e)}")
        return {
            "status": 500,
            "mensagem": "Erro interno ao listar seguidores com estatísticas"
        } 
        
# lista seguidos pleo usuairo
def controller_listar_seguidos_com_estatisticas(usuario_id: int):
    try:
        seguidos = model_listar_seguidos_com_estatisticas(usuario_id)

        return {
            "status": 200,
            "mensagem": "Seguidos listados com sucesso",
            "seguidos": seguidos
        }

    except Exception as e:
        logger.error(f"Erro ao listar seguidos com estatísticas para o usuário {usuario_id}: {str(e)}")
        return {
            "status": 500,
            "mensagem": "Erro interno ao listar seguidos com estatísticas"
        }
    