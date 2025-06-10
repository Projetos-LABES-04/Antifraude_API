from datetime import datetime, timedelta
from app.db.database import db
from typing import Optional

async def contar_transacoes_periodo(periodo_inicio: Optional[datetime], periodo_fim: Optional[datetime]) -> dict:
    transacoes_col = db["todo_collection"]

    if periodo_inicio and periodo_fim:
        dias = []
        data_atual = periodo_inicio
        while data_atual <= periodo_fim:
            dias.append(data_atual.strftime("%Y-%m-%d "))
            data_atual += timedelta(days=1)

        filtro_data = {
            "$or": [{"transacao_data": {"$regex": f"^{dia}"}} for dia in dias]
        }
    else:
        filtro_data = {}

    print("📅 Dias utilizados no filtro:", dias)
    print("🔎 Filtro montado:", filtro_data)

    total = await transacoes_col.count_documents(filtro_data)
    return {"quantidade_transacoes": total}
