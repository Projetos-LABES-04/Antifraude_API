from fastapi import APIRouter, HTTPException
from app.db.database import db
from app.schemas.auth_schema import LoginInput
from app.utils.auth_utils import verificar_senha, gerar_token

router = APIRouter()

@router.post("/login")
async def login(dados: LoginInput):
    usuario = await db["usuarios"].find_one({"matricula": dados.matricula})
    
    if not usuario or not verificar_senha(dados.senha, usuario["hashed_senha"]):
        raise HTTPException(status_code=401, detail="Matrícula ou senha inválidos.")
    
    token = gerar_token({"sub": usuario["matricula"], "nome": usuario["nome"]})
    return {"access_token": token, "token_type": "bearer"}