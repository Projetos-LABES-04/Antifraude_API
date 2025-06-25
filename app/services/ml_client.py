 # Cliente responsável por se comunicar com o serviço ML
import httpx
from datetime import datetime

ML_API_URL = "https://web-production-995a.up.railway.app/inferencia"

async def chamar_servico_ml(transacao: dict) -> dict:
    try:
        if isinstance(transacao["transacao_data"], datetime):
            transacao["transacao_data"] = transacao["transacao_data"].isoformat()

        payload = {
            "transacao_id": str(transacao["transacao_id"]),
            "cliente_id": int(transacao["cliente_id"]),
            "conta_id": str(transacao["conta_id"]),
            "conta_destino_id": str(transacao["conta_destino_id"]),
            "mesma_titularidade": bool(transacao["mesma_titularidade"]),
            "transacao_data": str(transacao["transacao_data"]),
            "transacao_valor": float(transacao["transacao_valor"]),
            "transacao_tipo": str(transacao["transacao_tipo"])
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(ML_API_URL, json=[payload])
            response.raise_for_status()
            return response.json()["amostra"][0]

    except httpx.HTTPStatusError as e:
        print("Erro ao enviar para /inferencia:")
        print(payload)
        print("Erro:", e.response.text)
        raise
