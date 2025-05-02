from pydantic import BaseModel
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