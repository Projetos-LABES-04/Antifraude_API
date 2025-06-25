 # Cliente responsável por se comunicar com o serviço ML
import httpx

ML_API_URL = "https://web-production-995a.up.railway.app/inferencia"

async def chamar_servico_ml(transacao: dict) -> dict:
    # Garante que a data esteja no formato ISO
    if isinstance(transacao["transacao_data"], datetime):
        transacao["transacao_data"] = transacao["transacao_data"].isoformat()

    # Monta o payload com apenas os campos esperados
    payload = {
        "transacao_id": transacao["transacao_id"],
        "cliente_id": transacao["cliente_id"],
        "conta_id": transacao["conta_id"],
        "conta_destino_id": transacao["conta_destino_id"],
        "mesma_titularidade": transacao["mesma_titularidade"],
        "transacao_data": transacao["transacao_data"],
        "transacao_valor": transacao["transacao_valor"],
        "transacao_tipo": transacao["transacao_tipo"]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(ML_API_URL, json=[payload])  # Lista com uma transação
        response.raise_for_status()
        return response.json()["amostra"][0]  # Retorna o primeiro item da resposta