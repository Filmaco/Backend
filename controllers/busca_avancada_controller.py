from models.busca_avancada_model import (
    model_listar_videos_por_tipo,
    model_buscar_videos_avancado,
    )
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

def controller_buscar_videos_avancado(
    nome: str = None,
    generos: List[str] = None,
    tags: list = None,
    tipos: List[str] = None,
    data_inicio: str = None,
    data_fim: str = None,
    duracao: str = None
):
    try:
        resultados = model_buscar_videos_avancado(
            nome=nome,
            generos=generos,
            tags=tags,
            tipos=tipos,
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


def controller_listar_videos_por_tipo(tipo):
    try:
        videos = model_listar_videos_por_tipo(tipo)
        return {"status": 200, "data": videos}
    except Exception as e:
        logger.error(f"Erro ao listar vídeos do tipo {tipo}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar vídeos"}