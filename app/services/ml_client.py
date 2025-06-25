 # Cliente responsável por se comunicar com o serviço ML
import httpx

ML_API_URL = "https://web-production-995a.up.railway.app/inferencia"

async def chamar_servico_ml(transacao: dict) -> int:
    
    payload = {
        "transacao_id": "abc123",
        "cliente_id": 101,
        "conta_id": "c1",
        "conta_destino_id": "c2",
        "mesma_titularidade": False,
        "transacao_data": "2023-08-01T08:15:00",
        "transacao_valor": 1250.0,
        "transacao_tipo": "pix",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(ML_API_URL, json=payload)
        response.raise_for_status()
        return response.json()["fraude"]  # Espera 0 ou 1
