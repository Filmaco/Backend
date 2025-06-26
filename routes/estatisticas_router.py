from controllers.estatistica_controller import (
    controller_obter_estatisticas_usuario,
    controller_listar_seguidores_com_estatisticas,
    controller_listar_seguidos_com_estatisticas,
    controller_obter_estatisticas_usuario_avancado,
    controller_obter_estatisticas_admin
)
from pydantic import BaseModel
from typing import Optional
import os
from typing import Optional, List, Union
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form

router = APIRouter(prefix="/estatisticas", tags=["Estatisticas"])

# -------------------- USUARIO COMUM ---------------

# estatisticas basicas usuario comum
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
    
# estatisticas avancadas
@router.get("/usuarios/{usuario_id}/detalhado", status_code=status.HTTP_200_OK)
async def obter_estatisticas_usuario_detalhado(usuario_id: int):
    try:
        response = controller_obter_estatisticas_usuario_avancado(usuario_id)
        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas detalhadas: {str(e)}")


# -------------------- ADMIN ---------------

# estatisticas admin
@router.get("/admin", status_code=status.HTTP_200_OK)
async def obter_estatisticas_admin():
    try:
        response = controller_obter_estatisticas_admin()
        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas administrativas: {str(e)}")