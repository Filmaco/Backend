from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from controllers.usuario_controller import (
    controller_criar_usuario,
    controller_listar_usuarios,
    controller_atualizar_usuario,
    controller_inativar_usuario,
    controller_login
)
from models.usuario_model import model_obter_usuario_por_id
import jwt
from pydantic import BaseModel, EmailStr
import requests
import os
import firebase_admin
from firebase_admin import credentials

# Inicializando o Firebase Admin
service_account_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "serviceAccountKey.json")
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)

SECRET_KEY = "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"
FIREBASE_API_KEY = "AIzaSyBX-lCLKQ3BSzZEhkDqZqpGzwg6nFbKU_0"

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

class ResetSenhaRequest(BaseModel):
    email: EmailStr

# Adicionar Usuario
@router.post("/usuarios/add", status_code=status.HTTP_201_CREATED)
async def criar_usuario(data: dict):
    try:
        response = controller_criar_usuario(data)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Editar Usuario
@router.put("/usuarios/editar/{usuario_id}", status_code=status.HTTP_200_OK)
async def atualizar_usuario(usuario_id: int, data: dict):
    try:
        response = controller_atualizar_usuario(usuario_id, data)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Inativar Usuario
@router.put("/usuarios/inativar/{usuario_id}", status_code=status.HTTP_200_OK)
async def alterar_status_usuario(usuario_id: int, data: dict):
    status_usuario = data.get("status", "inativo")
    try:
        response = controller_inativar_usuario(usuario_id, status_usuario)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Listar Usuarios
@router.get("/usuarios", status_code=status.HTTP_200_OK)
async def obter_usuarios():
    try:
        response = controller_listar_usuarios()
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Login
@router.post("/usuarios/login", status_code=status.HTTP_200_OK)
async def login(data: dict):
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email e senha são obrigatórios")

    try:
        token = controller_login(email, senha)
        if token:
            return {"mensagem": "Login realizado com sucesso", "token": token}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Verifica o token de login
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        usuario_id = payload.get("usuario_id")
        if usuario_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return usuario_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

# Perfil do usuário
@router.get("/perfil", status_code=status.HTTP_200_OK)
async def obter_usuario_logado(usuario_id: int = Depends(verificar_token)):
    try:
        usuario = model_obter_usuario_por_id(usuario_id)
        if usuario:
            return {"usuario": usuario}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Resetar Senha
@router.post("/resetar/senha")
async def resetar_senha(request: ResetSenhaRequest):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        try:
            error_detail = response.json()
            error_message = error_detail.get("error", {}).get("message", "Erro desconhecido")
        except Exception as e:
            error_message = f"Erro ao enviar email: {e}"

        print(f"Erro ao tentar resetar a senha: {error_message}")
        raise HTTPException(status_code=400, detail=error_message)

    return {"message": "Email de redefinição enviado com sucesso"}
