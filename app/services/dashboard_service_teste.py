from datetime import datetime, timedelta
from app.db.database import db

async def contar_transacoes_periodo(periodo_inicio: datetime, periodo_fim: datetime) -> dict:
    transacoes_col = db["transacoes"]

    dias = []
    data_atual = periodo_inicio
    while data_atual <= periodo_fim:
        dias.append(data_atual.strftime("%Y-%m-%d"))
        data_atual += timedelta(days=1)

    filtro_data = {
    "$expr": {
        "$in": [
            { "$substr": ["$transacao_data", 0, 10] },
            dias
        ]
    }
}


    print("📅 Dias utilizados no filtro:", dias)
    print("🔍 Regex usada:", f"^({'|'.join(dias)})")

    total = await transacoes_col.count_documents(filtro_data)
    return {"quantidade_transacoes": total}

