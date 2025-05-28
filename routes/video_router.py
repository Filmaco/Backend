# routers/video_router.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from controllers.video_controller import (
    controller_criar_video,
    controller_obter_video_por_id,
    controller_atualizar_video,
    controller_listar_videos_por_usuario,
    controller_incrementar_visualizacoes,
    controller_listar_videos,
    controller_listar_videos_por_tipo,
    controller_criar_tags,
    controller_listar_videos_por_tag,
    controller_listar_tags,
    controller_listar_videos_por_genero,
    controller_inativar_video,
    controller_obter_nome_tag_por_id
)
from pydantic import BaseModel
from typing import Optional
import os
from typing import Optional, List, Union


router = APIRouter(prefix="/videos", tags=["Videos"])

class VideoCreate(BaseModel):
    usuario_id: int
    nome: str
    genero: str
    duracao: str
    tipo: str
    link: str
    descricao: Optional[str] = None
    imagem: Optional[UploadFile] = File(None)

    class Config:
        orm_mode = True

class VideoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    genero: Optional[str] = None
    duracao: Optional[str] = None
    tipo: Optional[str] = None
    link: Optional[str] = None

# funcao para alterar link do youtue pra poder usar o player (iframe)
def transformar_youtube_para_embed(link: str) -> str:
    import re
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", link)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    return link

# verifica se tem tags
def processar_tags(tags: Optional[Union[str, List[str]]]) -> Optional[List[str]]:
    if tags is None:
        return None
    if isinstance(tags, list):
        return tags
    if isinstance(tags, str):
        return [tags]
    return None


# ------  CRUD VIDEO --------

#criar video
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def criar_video(
        usuario_id: int = Form(...),
        nome: str = Form(...),
        genero: str = Form(...),
        duracao: str = Form(...),
        tipo: str = Form(...),
        link: str = Form(...),
        descricao: Optional[str] = Form(None),
        tags: Optional[str] = Form(None),
        imagem: Optional[UploadFile] = File(None)
    ):
    try:
        link = transformar_youtube_para_embed(link)
        
        imagem_nome = None
        if imagem:
            import os
            os.makedirs("uploads", exist_ok=True)

            nome_arquivo = imagem.filename
            caminho = f"uploads/{nome_arquivo}"

            with open(caminho, "wb") as f:
                f.write(await imagem.read())

            imagem_nome = nome_arquivo

        dados = {
            "usuario_id": usuario_id,
            "nome": nome,
            "genero": genero,
            "duracao": duracao,
            "tipo": tipo,
            "link": link,
            "descricao": descricao,
            "imagem": imagem_nome,
            "tags": tags
        }

        response = controller_criar_video(dados)

        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])
        return response

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/editar/{video_id}", status_code=status.HTTP_200_OK)
async def atualizar_video(
    video_id: int,
    nome: str = Form(None),
    genero: str = Form(None),
    duracao: str = Form(None),
    tipo: str = Form(None),
    link: str = Form(None),
    descricao: str = Form(None),
    tags: List[str] = Form([]),
    imagem: Optional[UploadFile] = File(None)
):
    try:
        imagem_nome = None
        if imagem:
            os.makedirs("uploads", exist_ok=True)
            nome_arquivo = imagem.filename
            caminho = f"uploads/{nome_arquivo}"

            with open(caminho, "wb") as f:
                f.write(await imagem.read())

            imagem_nome = nome_arquivo

        dados = {
            "nome": nome,
            "genero": genero,
            "duracao": duracao,
            "tipo": tipo,
            "link": link,
            "descricao": descricao,
            "imagem": imagem_nome,
            "tags": tags
        }

        response = controller_atualizar_video(video_id, dados)

        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])

        return response

    except Exception as e:
        print(f"Erro ao atualizar vídeo: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado: {str(e)}")



# ----- VISUALIZACAO -----

#visualizacao
@router.post("/{video_id}/visualizacao", status_code=status.HTTP_200_OK)
async def incrementar_visualizacao(video_id: int):
    try:
        response = controller_incrementar_visualizacoes(video_id)
        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ------- LISTAR --------

# listar todos os videos
@router.get("/", status_code=status.HTTP_200_OK)
async def listar_videos():
    try:
        response = controller_listar_videos()
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# listar tags
@router.get("/tags", status_code=status.HTTP_200_OK)
async def listar_tags():
    try:
        response = controller_listar_tags()
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ------ LISTAR POR --------

# listar videos por usuario
@router.get("/usuario/{usuario_id}", status_code=status.HTTP_200_OK)
async def listar_videos_usuario(usuario_id: int):
    try:
        response = controller_listar_videos_por_usuario(usuario_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# listar videos por tipo
@router.get("/tipo/{tipo}", status_code=status.HTTP_200_OK)
async def listar_videos_tipo(tipo: str):
    try:
        response = controller_listar_videos_por_tipo(tipo)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#listar video por tag
@router.get("/tag/{nome_tag}", status_code=status.HTTP_200_OK)
async def listar_videos_por_tag(nome_tag: str):
    try:
        response = controller_listar_videos_por_tag(nome_tag)
        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#listar video por genero
@router.get("/genero/{genero}", status_code=status.HTTP_200_OK)
async def listar_videos_genero(genero: str):
    try:
        response = controller_listar_videos_por_genero(genero)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
 
 
# ------ VIDEO POR ID ------
    
# pegar video por id
@router.get("/{video_id}", status_code=status.HTTP_200_OK)
async def obter_video(video_id: int):
    try:
        response = controller_obter_video_por_id(video_id)
        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ----- INATIVAR -----

# inativar
@router.put("/inativar/{video_id}", status_code=status.HTTP_200_OK)
async def inativar_video(video_id: int):
    try:
        response = controller_inativar_video(video_id)
        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# -------------- TAGS --------------

#pesquisa tag por id
@router.get("/tag/id/{id_tag}", status_code=status.HTTP_200_OK)
async def obter_nome_tag_por_id(id_tag: int):
    try:
        response = controller_obter_nome_tag_por_id(id_tag)
        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
    
    
    
    
    
    
