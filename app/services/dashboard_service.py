from datetime import datetime, timedelta
from app.schemas.dashboard_schema import DashboardResumo
from app.db.database import db

async def obter_dashboard(periodo_inicio: datetime, periodo_fim: datetime) -> DashboardResumo:
    transacoes_col = db["transacoes"]

    # Converte o intervalo para strings no formato compatível
    dias = []
    data_atual = periodo_inicio
    while data_atual <= periodo_fim:
        dias.append(data_atual.strftime("%Y-%m-%d"))  # Formato de prefixo usado na string
        data_atual += timedelta(days=1)

    # Filtros para campos com data como string
    filtro_data = {"$or": [{"transacao_data": {"$regex": f"^{dia}"}} for dia in dias]}

    total_transacoes = await transacoes_col.count_documents(filtro_data)

    transacoes_suspeitas = await transacoes_col.count_documents({
        "status": "suspeita",
        **filtro_data
    })

    fraudes_confirmadas = await transacoes_col.count_documents({
        "status": "fraude_confirmada",
        **filtro_data
    })

    media_resultado = await transacoes_col.aggregate([
        {
            "$match": {
                "status": "suspeita",
                **filtro_data
            }
        },
        {
            "$group": {
                "_id": None,
                "media_valor": {"$avg": "$transacao_valor"}
            }
        }
    ]).to_list(length=1)

    valor_medio_suspeitas = media_resultado[0]["media_valor"] if media_resultado else 0.0

    return DashboardResumo(
        total_transacoes=total_transacoes,
        transacoes_suspeitas=transacoes_suspeitas,
        fraudes_confirmadas=fraudes_confirmadas,
        valor_medio_suspeitas=valor_medio_suspeitas
    )
