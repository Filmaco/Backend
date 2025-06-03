from fastapi import APIRouter, Form, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
from controllers.comentario_controller import (
    controller_adicionar_comentario,
    controller_listar_comentarios_por_video,
    controller_excluir_comentario
)
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])


# add comentario
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def adicionar_comentario(
    video_id: int = Form(...),
    usuario_id: int = Form(...),
    conteudo: str = Form(...)
):
    try:
        dados = {
            "video_id": video_id,
            "usuario_id": usuario_id,
            "conteudo": conteudo
        }

        response = controller_adicionar_comentario(dados)

        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])

        return JSONResponse(status_code=201, content=response)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# listar comentarios por video
@router.get("/video/{video_id}")
async def listar_comentarios(video_id: int):
    comentarios = controller_listar_comentarios_por_video(video_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(comentarios))

# excluir

@router.delete("/excluir/{comentario_id}/{usuario_id}")
async def excluir_comentario(comentario_id: int, usuario_id: int):
    response = controller_excluir_comentario(comentario_id, usuario_id)

    if response["status"] != 200:
        raise HTTPException(status_code=response["status"], detail=response["mensagem"])

    return JSONResponse(status_code=200, content=response)