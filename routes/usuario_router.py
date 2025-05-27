from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import BaseModel, EmailStr
import requests
import os
import firebase_admin
from firebase_admin import credentials
from fastapi import UploadFile, File, Form
from typing import Optional
from controllers.usuario_controller import (
    controller_criar_usuario,
    controller_listar_usuarios,
    controller_atualizar_usuario,
    controller_alterar_status_usuario,
    controller_login,
    controller_obter_usuario_por_name,
    controller_obter_usuario_por_id,
    controller_aterar_tipo_usuario,
)
from models.usuario_model import model_obter_usuario_por_id
from fastapi.responses import JSONResponse


SECRET_KEY = "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"

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

class ResetSenhaRequest(BaseModel):
    email: EmailStr


# ADD
@router.post("/usuarios/add", status_code=status.HTTP_201_CREATED)
async def criar_usuario(
    nome_completo: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    tipo: str = Form(...),
    biografia: str = Form(...),
    genero: str = Form(...),
    username: str = Form(...),
    data_nascimento: str = Form(...),

    foto_perfil: Optional[UploadFile] = File(None)
):
    try:
        foto_nome = None
        if foto_perfil:
            import os
            os.makedirs("uploads", exist_ok=True)

            nome_arquivo = foto_perfil.filename
            caminho = f"uploads/{nome_arquivo}"

            with open(caminho, "wb") as f:
                f.write(await foto_perfil.read())

            foto_nome = nome_arquivo

        dados = {
            "nome_completo": nome_completo,
            "email": email,
            "senha": senha,
            "foto_perfil": foto_nome,
            "biografia": biografia,
            "tipo": tipo,
            "genero": genero,
            "username": username,
            "data_nascimento": data_nascimento,
        }

        response = controller_criar_usuario(dados)

        if response["status"] != 200:
            raise HTTPException(status_code=response["status"], detail=response["mensagem"])

        return JSONResponse(status_code=201, content=response)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# EDITAR
@router.put("/usuarios/editar/{usuario_id}")
async def atualizar_usuario(
    usuario_id: int,
    nome_completo: str = Form(None),
    email: str = Form(None),
    senha: str = Form(None),
    username: str = Form(None),
    data_nascimento: str = Form(None),
    genero: str = Form(None),
    biografia: str = Form(None),
    foto_perfil: UploadFile = File(None)
):
    try:
        foto_nome = None
        if foto_perfil:
            import os
            os.makedirs("uploads", exist_ok=True)

            nome_arquivo = foto_perfil.filename
            caminho = f"uploads/{nome_arquivo}"

            with open(caminho, "wb") as f:
                f.write(await foto_perfil.read())

            foto_nome = nome_arquivo

        dados = {}

        if nome_completo is not None: dados["nome_completo"] = nome_completo
        if email is not None: dados["email"] = email
        if senha is not None: dados["senha"] = senha
        if username is not None: dados["username"] = username
        if data_nascimento is not None: dados["data_nascimento"] = data_nascimento
        if genero is not None: dados["genero"] = genero
        if biografia is not None: dados["biografia"] = biografia
        if foto_nome is not None: dados["foto_perfil"] = foto_nome

        if not dados:
            raise HTTPException(status_code=400, detail="Nenhum dado foi enviado para atualizar.")

        response = controller_atualizar_usuario(usuario_id, dados)
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ALTERAR STATUS
@router.put("/usuarios/status/{usuario_id}/{status}", status_code=status.HTTP_200_OK)
async def alterar_status_usuario(usuario_id, status,  data: dict):
    # status_usuario = data.get("status", "inativo")
    try:
        response = controller_alterar_status_usuario(usuario_id, status)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# TORNAR ADM
@router.put("/usuarios/promover/{admin_id}/{usuario_id_promovido}/{tipo}")
async def aterar_tipo_usuario(admin_id, usuario_id_promovido, tipo):
    try:
        resposta = controller_aterar_tipo_usuario(admin_id, usuario_id_promovido, tipo)
        return resposta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# LISTARs
@router.get("/usuarios", status_code=status.HTTP_200_OK)
async def obter_usuarios():
    try:
        response = controller_listar_usuarios()
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# LOGIN
@router.post("/usuarios/login", status_code=status.HTTP_200_OK)
async def login(data: dict):
    email = data.get("email")
    senha = data.get("senha")
    id = data.get("id")  

    if not email or not senha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email e senha são obrigatórios")

    try:
        token = controller_login(email, senha)
        if token:
            return {"mensagem": "Login realizado com sucesso", "token": token, "id": id}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
# VERIFICA TOKEN
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        usuario_id = payload.get("sub")  
        if usuario_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return usuario_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        usuario_id = payload.get("usuario_id")
        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"usuario_id": usuario_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail=f"Token inválido: {token}")


# PERFIL
@router.get("/perfil")
async def obter_perfil(usuario=Depends(get_current_user)):
    usuario_id = usuario["usuario_id"]
    
    dados = model_obter_usuario_por_id(usuario_id)
    if not dados:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {"usuario": dados}


# pegarusuario por nome
@router.get("/usuarios/nome/{nome_completo}")
async def obter_usuario_por_nome(nome_completo: str):
    try:
        dados = controller_obter_usuario_por_name(nome_completo)
        if not dados:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"usuario": dados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# pegar usuairo por ID
@router.get("/usuarios/{usuario_id}")
async def obter_usuario_por_id(usuario_id: int):
    resultado = controller_obter_usuario_por_id(usuario_id)

    try:
        resultado = controller_obter_usuario_por_id(usuario_id)
        if not resultado:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"usuario": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# # Resetar Senha
# @router.post("/resetar/senha")
# async def resetar_senha(request: ResetSenhaRequest):
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"
#     payload = {
#         "requestType": "PASSWORD_RESET",
#         "email": request.email
#     }

#     response = requests.post(url, json=payload)

#     if response.status_code != 200:
#         try:
#             error_detail = response.json()
#             error_message = error_detail.get("error", {}).get("message", "Erro desconhecido")
#         except Exception as e:
#             error_message = f"Erro ao enviar email: {e}"

#         print(f"Erro ao tentar resetar a senha: {error_message}")
#         raise HTTPException(status_code=400, detail=error_message)

#     return {"message": "Email de redefinição enviado com sucesso"}


