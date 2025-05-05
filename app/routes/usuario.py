from pydantic import BaseModel, field_validator
import re
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import Optional, Annotated
from app.services.usuario_service import usuario_service
from datetime import datetime
import logging

router = APIRouter(
    prefix="/usuario",
    tags=["usuario"]
)

# Configuração de logging
logger = logging.getLogger(__name__)

class UsuarioBase(BaseModel):
    nome: str
    criado_em: Optional[datetime] = None

class LoginModel(UsuarioBase):
    senha: str

    @field_validator('senha')
    def validar_senha(cls, v):
        if len(v) < 8:
            raise ValueError("Senha deve ter no mínimo 8 caracteres")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Senha deve conter pelo menos uma letra maiúscula")
        if not re.search(r'[a-z]', v):
            raise ValueError("Senha deve conter pelo menos uma letra minúscula")
        if not re.search(r'[0-9]', v):
            raise ValueError("Senha deve conter pelo menos um número")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Senha deve conter pelo menos um caractere especial")
        return v

class UsuarioResponse(UsuarioBase):
    id: str

@router.post('/login', response_model=UsuarioResponse)
async def login_usuario(data: LoginModel):
    """
    Autentica um usuário existente.
    
    - **nome**: Nome de usuário
    - **senha**: Senha (deve conter maiúsculas, minúsculas, números e caracteres especiais)
    """
    try:
        usuario = await usuario_service.autenticar_usuario(data.nome, data.senha)
        if not usuario:
            logger.warning(f"Tentativa de login falha para usuário: {data.nome}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=usuario
        )
    except Exception as e:
        logger.error(f"Erro no login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor"
        )

@router.post("/criar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def criar_usuario(data: LoginModel):
    """
    Cria um novo usuário no sistema.
    
    - **nome**: Nome de usuário único
    - **senha**: Senha forte (mínimo 8 caracteres com maiúsculas, minúsculas, números e especiais)
    """
    try:
        novo_usuario = await usuario_service.criar_usuario(data.nome, data.senha)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=novo_usuario
        )
    except ValueError as e:
        logger.warning(f"Tentativa de criar usuário existente: {data.nome}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao criar usuário"
        )