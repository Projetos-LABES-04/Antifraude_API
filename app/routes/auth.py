from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.utils.auth_utils import criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    senha: str

@router.post("/login")
async def login(data: LoginRequest):
    # 💡 Aqui você colocaria a VERDADEIRA checagem no banco
    if data.email == "usuario@empresa.com" and data.senha == "123456":
        # Gera o token JWT contendo o email como identificação
        token = criar_token({"sub": data.email})
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")