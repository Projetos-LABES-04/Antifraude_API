# routers/notificacoes.py

from fastapi import APIRouter, HTTPException
from typing import List
from schemas.notificacao_schema import NotificacaoBase
from db import db  # Isso depende da sua estrutura de conexão

router = APIRouter()

@router.post("/notificacoes")
async def criar_notificacao(notificacao: NotificacaoBase):
    resultado = await db["notificacoes"].insert_one(notificacao.dict())
    if resultado.inserted_id:
        return {"msg": "Notificação criada", "id": str(resultado.inserted_id)}
    raise HTTPException(status_code=500, detail="Erro ao criar notificação")

@router.get("/notificacoes", response_model=List[NotificacaoBase])
async def listar_notificacoes():
    notificacoes = await db["notificacoes"].find().to_list(100)
    return notificacoes
