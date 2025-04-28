from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from controllers.video_controller import (
    controller_criar_video,
    controller_obter_video_por_id,
    controller_atualizar_video,
    controller_listar_videos_por_usuario,
    controller_incrementar_visualizacoes,
    controller_listar_videos,
    controller_listar_videos_por_tipo
)
from pydantic import BaseModel
from typing import Optional
import jwt


router = APIRouter(prefix="/videos", tags=["Videos"])

class VideoCreate(BaseModel):
    usuario_id: int
    nome: str
    genero: str
    duracao: str
    tipo: str
    link: str
    descricao: Optional[str] = None
    tags: Optional[str] = None

class VideoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    genero: Optional[str] = None
    tags: Optional[str] = None
    duracao: Optional[str] = None
    tipo: Optional[str] = None
    link: Optional[str] = None


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def criar_video(video: VideoCreate):
    try:
        response = controller_criar_video(video.dict())
        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/editar/{video_id}", status_code=status.HTTP_200_OK)
async def atualizar_video(video_id: int, video: VideoUpdate):
    try:
        response = controller_atualizar_video(video_id, video.dict(exclude_unset=True))
        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{video_id}", status_code=status.HTTP_200_OK)
async def obter_video(video_id: int):
    try:
        response = controller_obter_video_por_id(video_id)
        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/tipo/{tipo}", status_code=status.HTTP_200_OK)
async def listar_videos_tipo(tipo: str):
    try:
        response = controller_listar_videos_por_tipo(tipo)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK)
async def listar_videos():
    try:
        response = controller_listar_videos()
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{video_id}/visualizacao", status_code=status.HTTP_200_OK)
async def incrementar_visualizacao(video_id: int):
    try:
        response = controller_incrementar_visualizacoes(video_id)
        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
@router.get("/usuario/{usuario_id}", status_code=status.HTTP_200_OK)
async def listar_videos_usuario(usuario_id: int):
    try:
        response = controller_listar_videos_por_usuario(usuario_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))