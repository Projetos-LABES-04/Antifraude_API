from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from app.services.dashboard_service_teste import contar_transacoes_periodo

router = APIRouter()


@router.get("/dashboard/quantidade_transacoes")
async def contar_transacoes(
    periodo_inicio: datetime = Query(..., description="Data inicial (ex: 2023-01-01T00:00:00)"),
    periodo_fim: datetime = Query(..., description="Data final (ex: 2023-01-01T23:59:59)")
):
    return await contar_transacoes_periodo(periodo_inicio, periodo_fim)