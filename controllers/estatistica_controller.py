from models.estatistica_model import (
    model_obter_estatisticas_usuario
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