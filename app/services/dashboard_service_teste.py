from datetime import datetime, timedelta
from app.db.database import db

async def contar_transacoes_periodo(periodo_inicio: datetime, periodo_fim: datetime) -> dict:
    transacoes_col = db["todo_collection"]

    # formato YYYY-MM-DD
    dias = []
    data_atual = periodo_inicio
    while data_atual <= periodo_fim:
        dias.append(data_atual.strftime("%Y-%m-%d "))
        data_atual += timedelta(days=1)

    filtro_data = {
        "$or": [{"transacao_data": {"$regex": f"^{dia}"}} for dia in dias]
    }

    print("📅 Dias utilizados no filtro:", dias)
    print("🔎 Filtro montado:", filtro_data)

    total = await transacoes_col.count_documents(filtro_data)
    return {"quantidade_transacoes": total}
