from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
import os
from controllers.playlist_controller import (
    controller_criar_playlist,
    controller_listar_playlists_por_usuario,
    controller_adicionar_video_na_playlist,
    controller_listar_videos_da_playlist,
    controller_atualizar_playlist,
    controller_listar_playlist,
    controller_obter_playlist_por_id,
    controller_inativar_playlist
)

router = APIRouter(prefix="/playlists", tags=["Playlists"])

# ------------- PLAYLIST ------------

#add playlist
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def criar_playlist(
    usuario_id: int = Form(...),
    titulo: str = Form(...),
    imagem: UploadFile = File(None)
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
            "usuario_id": usuario_id,
            "titulo": titulo,
            "imagem": imagem_nome
        }

        response = controller_criar_playlist(dados)

        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])

        print("Resposta da controller:", response)
        return response

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado: {str(e)}")

# eidtar playlist
@router.put("/editar/{playlist_id}")
async def atualizar_usuario(
    playlist_id: int,
    titulo: str = Form(None),
    imagem: UploadFile = File(None)
):
    try:
        foto_nome = None
        if imagem:
            import os
            os.makedirs("uploads", exist_ok=True)

            nome_arquivo = imagem.filename
            caminho = f"uploads/{nome_arquivo}"

            with open(caminho, "wb") as f:
                f.write(await imagem.read())

            foto_nome = nome_arquivo

        dados = {}

        if titulo is not None: dados["titulo"] = titulo
        if foto_nome is not None: dados["imagem"] = foto_nome

        if not dados:
            raise HTTPException(status_code=400, detail="Nenhum dado foi enviado para atualizar.")

        response = controller_atualizar_playlist(playlist_id, dados)
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
# inativar
@router.put("/inativar/{playlist_id}", status_code=status.HTTP_200_OK)
async def alterar_status_playlist(playlist_id: int, data: dict):
    status_playlist = data.get("status", "inativo")
    try:
        response = controller_inativar_playlist(playlist_id, status_playlist)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

 
 
# listar playlists
@router.get("/", status_code=status.HTTP_200_OK)
async def listar_playlists():
    try:
        response = controller_listar_playlist()
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   
    
# listar playlist por usuario
@router.get("/usuario/{usuario_id}", status_code=status.HTTP_200_OK)
async def listar_playlists_usuario(usuario_id: int):
    try:
        response = controller_listar_playlists_por_usuario(usuario_id)

        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])

        return response

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado: {str(e)}")
   
# pegar playlist por ID
@router.get("/{playlist_id}")
async def obter_playlist_por_id(playlist_id: int):
    resultado = controller_obter_playlist_por_id(playlist_id)

    try:
        resultado = controller_obter_playlist_por_id(playlist_id)
        if not resultado:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"playlist": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------- PLAYLIST VIDEO ------------
 
# add video na plyalit
@router.post("/video/add", status_code=status.HTTP_201_CREATED)
async def adicionar_video_na_playlist(
    playlist_id: int = Form(...),
    video_id: int = Form(...)
):
    try:
        dados = {
            "playlist_id": playlist_id,
            "video_id": video_id
        }

        response = controller_adicionar_video_na_playlist(dados)

        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])

        return response

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado: {str(e)}")

# lista os videos da playlist
@router.get("/{playlist_id}/videos", status_code=status.HTTP_200_OK)
async def listar_videos_da_playlist(playlist_id: int):
    try:
        response = controller_listar_videos_da_playlist(playlist_id)

        if response["status"] != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["mensagem"])

        return response

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado: {str(e)}")

