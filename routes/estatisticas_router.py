from controllers.estatistica_controller import (
    controller_obter_estatisticas_usuario,
    controller_listar_seguidores_com_estatisticas,
    controller_listar_seguidos_com_estatisticas,
)
from pydantic import BaseModel
from typing import Optional
import os
from typing import Optional, List, Union
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form

router = APIRouter(prefix="/estatisticas", tags=["Estatisticas"])


@router.get("/usuarios/{usuario_id}", status_code=status.HTTP_200_OK)
async def obter_estatisticas_usuario(usuario_id: int):
    try:
        response = controller_obter_estatisticas_usuario(usuario_id)
        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")
    
# seguidores pelo usuairo
@router.get("/seguidores/{usuario_id}", status_code=status.HTTP_200_OK)
async def listar_seguidores_com_estatisticas(usuario_id: int):
    try:
        response = controller_listar_seguidores_com_estatisticas(usuario_id)
        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar seguidores com estatísticas: {str(e)}")

# seguidos pelo usuairo
@router.get("/seguidos/{usuario_id}", status_code=status.HTTP_200_OK)
async def listar_seguidos_com_estatisticas(usuario_id: int):
    try:
        response = controller_listar_seguidos_com_estatisticas(usuario_id)
        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar seguidos com estatísticas: {str(e)}")
