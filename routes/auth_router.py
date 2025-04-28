from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from controllers.usuario_controller import controller_login
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "chave-secreta-para-resetar-senha"
RESET_SECRET_KEY = "chave-secreta-diferente-para-reset-de-senha"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

router = APIRouter()

# model pra facilitar
class LoginRequest(BaseModel):
    email: str
    senha: str


# login
@router.post("/usuarios/login", status_code=status.HTTP_200_OK)
async def login(data: LoginRequest):
    try:
        token = controller_login(data.email, data.senha)
        if token:
            return {"mensagem": "Login realizado com sucesso", "token": token}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# verifica token
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        usuario_id = payload.get("usuario_id")
        if usuario_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return usuario_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
