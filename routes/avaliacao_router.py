from fastapi import APIRouter, Form, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
from controllers.avaliacao_controller import (
    controller_adicionar_avaliacao,
    controller_excluir_avaliacao,
    controller_listar_avaliacao,
    controller_atualizar_avaliacao
)
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/avaliacoes", tags=["Avaliacoes"])

# add avaliacao
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def adicionar_avaliacao(
    usuario_id: int = Form(...),
    video_id: int = Form(...),
    avaliacao: str = Form(...)
):
    try:
        dados = {
            "video_id": video_id,
            "usuario_id": usuario_id,
            "avaliacao": avaliacao
        }

        response = controller_adicionar_avaliacao(dados)

        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])

        return JSONResponse(
            status_code=201,
            content={
                "mensagem": response["mensagem"],
                "id": response["data"]["id"]
            }
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# totais avaliacao por video
    
# listar videos
@router.get("/listar/{video_id}", status_code=status.HTTP_200_OK)
async def listar_videos(video_id: int):
    try:
        response = controller_listar_avaliacao(video_id)
        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# excluir
@router.delete("/excluir/{avaliacao_id}")
async def excluir_avaliacao(avaliacao_id: int):
    response = controller_excluir_avaliacao(avaliacao_id)

    if response["status"] != 200:
        raise HTTPException(status_code=response["status"], detail=response["mensagem"])

    return JSONResponse(status_code=200, content=response)

# fazer o editar
@router.put("/editar/{avaliacao_id}")
async def atualizar_avaliacao(
    avaliacao_id: int,
    avaliacao: str = Form(None),
):
    try:
        dados = {}

        if avaliacao is not None: dados["avaliacao"] = avaliacao

        if not dados:
            raise HTTPException(status_code=400, detail="Nenhum dado foi enviado para atualizar.")

        response = controller_atualizar_avaliacao(avaliacao_id, dados)
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))