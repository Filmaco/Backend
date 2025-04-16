from fastapi import APIRouter
from controllers.usuario_controller import (
    controller_criar_usuario,
    controller_listar_usuarios,
    controller_atualizar_usuario,
    controller_inativar_usuario,
)


router = APIRouter()

#Adicionar
@router.post("/usuarios/add")
async def criar_usuario(data: dict):
    controller_criar_usuario(data)
    return {"mensagem": "Usuário criado com sucesso"}

#Editar
@router.put("/usuarios/editar/{usuario_id}")
async def atualizar_usuario(usuario_id: int, data: dict):
    controller_atualizar_usuario(usuario_id, data)
    return {"mensagem": "Usuário atualizado com sucesso"}

#Inativar
@router.put("/usuarios/inativar/{usuario_id}")
async def alterar_status_usuario(usuario_id: int, data: dict):
    status = data.get("status", "inativo") 
    sucesso = controller_inativar_usuario(usuario_id, status)
    if sucesso:
        return {"mensagem": "Usuário inativado com sucesso"}
    return {"mensagem": "Erro ao inativar usuário"}

#Listar
@router.get("/usuarios")
async def obter_usuarios():
    usuarios = controller_listar_usuarios()
    return {"usuarios": usuarios}