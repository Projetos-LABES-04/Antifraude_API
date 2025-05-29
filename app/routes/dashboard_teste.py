from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from app.services.dashboard_service_teste import contar_transacoes_periodo

@router.get("/dashboard/quantidade_transacoes")
async def get_quantidade_transacoes(
    periodo_inicio: str = Query(..., description="Data inicial (formato: YYYY-MM-DD)"),
    periodo_fim: str = Query(..., description="Data final (formato: YYYY-MM-DD)")
):
    try:
        data_inicio = datetime.strptime(periodo_inicio, "%Y-%m-%d")
        data_fim = datetime.strptime(periodo_fim, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")
    
    return await contar_transacoes_periodo(data_inicio, data_fim)