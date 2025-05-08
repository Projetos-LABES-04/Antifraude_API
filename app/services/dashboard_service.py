from datetime import datetime
from app.schemas.dashboard_schema import DashboardResumo, AlertaRecente
from app.db.database import db
  

async def obter_dashboard(periodo_inicio: datetime, periodo_fim: datetime) -> DashboardResumo:
    transacoes_col = db["transacoes"]
    contas_col = db["contas"]
    alertas_col = db["alertas"]  # ajuste se o nome for diferente

    #  Total de transações
    total_transacoes = await transacoes_col.count_documents({
        "data": {"$gte": periodo_inicio, "$lte": periodo_fim}
    })

    #  Transações suspeitas
    transacoes_suspeitas = await transacoes_col.count_documents({
        "status": "suspeita",
        "data": {"$gte": periodo_inicio, "$lte": periodo_fim}
    })

    #  Contas investigadas
    contas_investigadas = await contas_col.count_documents({
        "status": "investigada",
        "data_investigacao": {"$gte": periodo_inicio, "$lte": periodo_fim}
    })

    #  Fraudes confirmadas
    fraudes_confirmadas = await transacoes_col.count_documents({
        "status": "fraude_confirmada",
        "data": {"$gte": periodo_inicio, "$lte": periodo_fim}
    })

    #  Alertas recentes (últimos 5)
    alertas_cursor = alertas_col.find().sort("timestamp", -1).limit(5)
    alertas_list = await alertas_cursor.to_list(length=5)
    alertas = [
        AlertaRecente(
            mensagem=alerta["mensagem"],
            timestamp=alerta["timestamp"]
        )
        for alerta in alertas_list
    ]

    return DashboardResumo(
        total_transacoes=total_transacoes,
        transacoes_suspeitas=transacoes_suspeitas,
        contas_investigadas=contas_investigadas,
        fraudes_confirmadas=fraudes_confirmadas,
        alertas_recentes=alertas
    )
