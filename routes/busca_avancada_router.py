from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from typing import Optional, List
from controllers.busca_avancada_controller import (
    controller_listar_videos_por_tipo,
    controller_buscar_videos_avancado
    )

router = APIRouter(prefix="/busca", tags=["Busca Avançada"])

@router.get("/videos", status_code=200)
async def buscar_videos_avancado(
    nome: Optional[str] = None,
    generos: Optional[List[str]] = Query(default=None),
    tipos: Optional[List[str]] = Query(default=None),
    tags: Optional[List[str]] = Query(default=None),
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    duracao: Optional[str] = None
):
    try:
        response = controller_buscar_videos_avancado(
            nome=nome,
            generos=generos,
            tags=tags,
            tipos=tipos,
            data_inicio=data_inicio,
            data_fim=data_fim,
            duracao=duracao
        )

        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar vídeos: {str(e)}")

# listar videos por tipo
@router.get("/tipo/{tipo}", status_code=status.HTTP_200_OK)
async def listar_videos_tipo(tipo: str):
    try:
        response = controller_listar_videos_por_tipo(tipo)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))