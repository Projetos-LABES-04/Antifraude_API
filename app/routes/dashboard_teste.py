from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional
from app.db.database import db
from app.services.dashboard_service_teste import contar_transacoes_periodo

router = APIRouter()


@router.get("/dashboard/quantidade_transacoes")
async def quantidade_transacoes(
    periodo_inicio: Optional[datetime] = Query(None, description="Data inicial (ex: 2023-01-01)"),
    periodo_fim: Optional[datetime] = Query(None, description="Data final (ex: 2023-01-03)")
):
    return await contar_transacoes_periodo(periodo_inicio, periodo_fim)

@router.get("/notificacoes/quantidade")
async def contar_notificacoes():
    notificacoes = db["notificacoes"]
    quantidade = await notificacoes.count_documents({})
    return {"quantidade": quantidade}