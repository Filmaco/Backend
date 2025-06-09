from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from controllers.busca_avancada_controller import (
    controller_buscar_videos_avancado,
    )

router = APIRouter(prefix="/busca", tags=["Busca Avançada"])

@router.get("/videos", status_code=200)
async def buscar_videos_avancado(
    nome: Optional[str] = None,
    genero: Optional[str] = None,
    tags: Optional[List[str]] = Query(default=None),
    tipo: Optional[str] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    duracao: Optional[str] = None
):
    try:
        response = controller_buscar_videos_avancado(
            nome=nome,
            genero=genero,
            tags=tags,
            tipo=tipo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            duracao=duracao
        )

        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar vídeos: {str(e)}")
