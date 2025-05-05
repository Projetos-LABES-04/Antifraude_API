from pydantic import BaseModel, field_validator
import re
from fastapi import HTTPException, status
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Optional



from fastapi import APIRouter

router = APIRouter(
    prefix="/usuario",
    tags=["usuario"]
)



class LoginModel(BaseModel):
    nome: str
    senha: str

@field_validator('senha')
def validar_senha(cls, v):
        # Verifica se há pelo menos um caractere especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("A senha deve conter pelo menos um caractere especial")
        # Verifica se há pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', v):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        # Verifica se há pelo menos uma letra minúscula
        if not re.search(r'[a-z]', v):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula")
        # Verifica se há pelo menos um número
        if not re.search(r'[0-9]', v):
            raise ValueError("A senha deve conter pelo menos um número")
        # Verifica o comprimento mínimo
        if len(v) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres")
        return v





@router.post('/login')
def login_usuario(data: LoginModel):
    try:
        usuario = usuario_service.autenticar_usuario(data.nome, data.senha)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nome ou senha inválidos"
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"mensagem": "Login realizado com sucesso", "usuario": usuario}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


def autenticar_usuario(self, nome: str, senha: str) -> Optional[dict]:
    usuario = self.db.find_one({"nome": nome})
    if usuario and usuario["senha"] == senha:
        return usuario  # ou sanitize antes de retornar
    return None