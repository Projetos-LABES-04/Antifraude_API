 # Cliente responsável por se comunicar com o serviço ML
import httpx

ML_API_URL = "https://web-production-0e5e.up.railway.app/predict" 

async def chamar_servico_ml(transacao: dict) -> int:
    
    payload = {
        "transacao_valor": transacao["transacao_valor"],
        "fim_de_semana": transacao["fim_de_semana"],
        "transacao_tipo_pix": transacao["transacao_tipo_pix"],
        "transacao_tipo_transferencia": transacao["transacao_tipo_transferencia"],
        "erro_reconstrucao": transacao["erro_reconstrucao"],
        "distancia_cluster": transacao["distancia_cluster"],
        "mesma_titularidade": transacao["mesma_titularidade"],
        "faixa_horaria_Madrugada": transacao["faixa_horaria_Madrugada"],
        "dia_de_semana_Sabado": transacao["dia_de_semana_Sabado"],
        "dia_de_semana_Domingo": transacao["dia_de_semana_Domingo"]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(ML_API_URL, json=payload)
        response.raise_for_status()
        return response.json()["fraude"]  # Espera 0 ou 1
