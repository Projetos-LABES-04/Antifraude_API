 # Cliente responsável por se comunicar com o serviço ML
import httpx

ML_API_URL = "https://web-production-995a.up.railway.app/inferencia"

async def chamar_servico_ml(transacao: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(ML_API_URL, json=[transacao])  # Lista com uma transação
        response.raise_for_status()
        resultado = response.json()["amostra"][0]  # Pega o 1º resultado
        return resultado