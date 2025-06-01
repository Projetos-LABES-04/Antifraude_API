from fastapi import APIRouter, Query
from datetime import datetime
from app.services.dashboard_service_teste import contar_transacoes_periodo

router = APIRouter()

@router.get("/dashboard/quantidade_transacoes")
async def quantidade_transacoes(
    periodo_inicio: datetime = Query(..., description="Data inicial (ex: 2023-01-01)"),
    periodo_fim: datetime = Query(..., description="Data final (ex: 2023-01-03)")
):
    return await contar_transacoes_periodo(periodo_inicio, periodo_fim)
