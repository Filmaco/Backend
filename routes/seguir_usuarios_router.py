from fastapi import APIRouter, HTTPException, status
from controllers.seguir_usuarios_controller import (
    controller_seguir_usuario,
    controller_deixar_de_seguir,
    controller_listar_seguidores,
)
router = APIRouter(prefix="/seguidores", tags=["Seguidores"])

# seguir
@router.post("/seguir/{seguidor_id}/{seguido_id}", status_code=status.HTTP_200_OK)
async def seguir_usuario(seguidor_id: int, seguido_id: int):
    try:
        response = controller_seguir_usuario(seguidor_id, seguido_id)
        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# deixar de seguir
@router.post("/deixar_de_seguir/{seguidor_id}/{seguido_id}", status_code=status.HTTP_200_OK)
async def deixar_de_seguir_usuario(seguidor_id: int, seguido_id: int):
    try:
        response = controller_deixar_de_seguir(seguidor_id, seguido_id)
        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# listar seguidores
@router.get("/listar/{usuario_id}", status_code=status.HTTP_200_OK)
async def listar_seguidores(usuario_id: int):
    try:
        response = controller_listar_seguidores(usuario_id)
        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))