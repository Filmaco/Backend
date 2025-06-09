from models.busca_avancada_model import (
    model_buscar_videos_avancado,
    )
import logging

logger = logging.getLogger(__name__)

def controller_buscar_videos_avancado(
    nome: str = None,
    genero: str = None,
    tags: list = None,
    tipo: str = None,
    data_inicio: str = None,
    data_fim: str = None,
    duracao: str = None
):
    try:
        resultados = model_buscar_videos_avancado(
            nome=nome,
            genero=genero,
            tags=tags,
            tipo=tipo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            duracao=duracao
        )

        return {
            "status": 200,
            "mensagem": "Vídeos encontrados com sucesso",
            "videos": resultados
        }

    except Exception as e:
        logger.error(f"Erro no controller_buscar_videos_avancado: {str(e)}")
        return {
            "status": 500,
            "mensagem": "Erro interno ao buscar vídeos"
        }
