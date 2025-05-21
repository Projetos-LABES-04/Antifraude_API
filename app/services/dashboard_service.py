from datetime import datetime
from app.schemas.dashboard_schema import DashboardResumo
from app.db.database import db

async def obter_dashboard(periodo_inicio: datetime, periodo_fim: datetime) -> DashboardResumo:
    transacoes_col = db["transacoes"]

    # Total de transações
    total_transacoes = await transacoes_col.count_documents({
        "data": {"$gte": periodo_inicio, "$lte": periodo_fim}
    })

    # Transações suspeitas
    transacoes_suspeitas = await transacoes_col.count_documents({
        "status": "suspeita",
        "data": {"$gte": periodo_inicio, "$lte": periodo_fim}
    })

    # Fraudes confirmadas
    fraudes_confirmadas = await transacoes_col.count_documents({
        "status": "fraude_confirmada",
        "data": {"$gte": periodo_inicio, "$lte": periodo_fim}
    })

    # Valor médio das transações suspeitas
    media_resultado = await transacoes_col.aggregate([
        {"$match": {
            "status": "suspeita",
            "data": {"$gte": periodo_inicio, "$lte": periodo_fim}
        }},
        {"$group": {"_id": None, "media_valor": {"$avg": "$valor"}}}
    ]).to_list(length=1)

    valor_medio_suspeitas = media_resultado[0]["media_valor"] if media_resultado else 0.0

    return DashboardResumo(
        total_transacoes=total_transacoes,
        transacoes_suspeitas=transacoes_suspeitas,
        fraudes_confirmadas=fraudes_confirmadas,
        valor_medio_suspeitas=valor_medio_suspeitas
    )
