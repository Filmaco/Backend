from fastapi import APIRouter, HTTPException, status, Body
from typing import Optional, Literal
from pydantic import BaseModel
from controllers.denuncia_controller import (
    controller_denunciar_conteudo,
    controller_listar_denuncias,
    controller_atualizar_status_denuncia,
    controller_remover_conteudo_denunciado,
    controller_alterar_status_video,
    controller_obter_denuncia_por_id
)
from models.denuncia_model import model_obter_denuncia_por_id


router = APIRouter(prefix="/denuncias", tags=["Denúncias"])

class DenunciaInput(BaseModel):
    usuario_id: int
    motivo: str
    video_id: Optional[int] = None

# denuncia o video
@router.post("/", status_code=status.HTTP_201_CREATED)
async def denunciar_conteudo(dados: DenunciaInput):
    response = controller_denunciar_conteudo(dados.dict())
    if response["status"] != 201:
        raise HTTPException(status_code=response["status"], detail=response["mensagem"])
    return response

# lista as denuncias
@router.get("/lista", status_code=status.HTTP_200_OK)
async def listar_denuncias():
    response = controller_listar_denuncias()
    if response["status"] != 200:
        raise HTTPException(status_code=response["status"], detail=response["mensagem"])
    return response


# atualiza o status da denuncia
@router.put("/{denuncia_id}/status", status_code=status.HTTP_200_OK)
async def atualizar_status_denuncia(
    denuncia_id: int,
    novo_status: Literal["pendente", "resolvido", "impedimento"] = Body(..., embed=True)
):
    response = controller_atualizar_status_denuncia(denuncia_id, novo_status)
    if response["status"] != 200:
        raise HTTPException(status_code=response["status"], detail=response["mensagem"])
    return response

# exclui de vez o video
@router.delete("/{denuncia_id}/remover-conteudo", status_code=status.HTTP_200_OK)
async def remover_conteudo_denunciado(denuncia_id: int):
    denuncia = model_obter_denuncia_por_id(denuncia_id)

    if not denuncia:
        raise HTTPException(status_code=404, detail="Denúncia não encontrada")

    response = controller_remover_conteudo_denunciado(denuncia)
    if response["status"] != 200:
        raise HTTPException(status_code=response["status"], detail=response["mensagem"])
    return response

# pega a denuncia pleo id
@router.get("/{denuncia_id}", status_code=status.HTTP_200_OK)
async def obter_denuncia_por_id(denuncia_id: int):

    response = controller_obter_denuncia_por_id(denuncia_id)
    if response["status"] != 200:
        raise HTTPException(status_code=response["status"], detail=response["mensagem"])
    return response

@router.put("/alterar-status/{video_id}/{status}", status_code=status.HTTP_200_OK)
async def alterar_status(video_id: int, status):

    response = controller_alterar_status_video(video_id, status)
    if response["status"] != 200:
        raise HTTPException(status_code=response["status"], detail=response["mensagem"])
    return response

