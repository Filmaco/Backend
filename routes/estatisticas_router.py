from controllers.estatistica_controller import controller_obter_estatisticas_usuario
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
