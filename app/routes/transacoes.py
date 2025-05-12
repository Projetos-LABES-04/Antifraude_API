from fastapi import APIRouter
from database.mongodb import collection
from services.ml_client import chamar_servico_ml


@router.post("/processar_pendentes")
async def processar_transacoes_sem_status():
    # Busca transações que ainda não têm status definido
    pendentes = await collection.find({"status": {"$exists": False}}).to_list(length=None)
    total = 0

    for transacao in pendentes:
        try:
            resultado = await chamar_servico_ml(transacao)
            status = "suspeito" if resultado == 1 else "normal"

            await collection.update_one(
                {"_id": transacao["_id"]},
                {"$set": {
                    "status": status,
                    "fraude_binario": resultado
                }}
            )
            total += 1
        except Exception as e:
            print(f"Erro na transação {transacao.get('transacao_id')}: {e}")

    return {"msg": f"{total} transações processadas com sucesso"}