from fastapi import APIRouter, Query
from datetime import datetime
from app.schemas.dashboard_schema import DashboardResumo
from app.services.dashboard_service import obter_dashboard

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResumo)
async def get_dashboard(
    periodo_inicio: datetime = Query(..., description="Data inicial do período (ex.: 2025-05-01T00:00:00)"),
    periodo_fim: datetime = Query(..., description="Data final do período (ex.: 2025-05-31T23:59:59)")
):
    return await obter_dashboard(periodo_inicio, periodo_fim)
