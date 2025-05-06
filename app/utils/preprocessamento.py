from datetime import datetime

def preprocessar_transacao(transacao_dict):
    """
    Recebe um dicionário de transação e transforma em formato tabular pronto para ML.
    """
    # Remover campos desnecessários
    transacao_dict.pop("_id", None)
    
    # Converter data para datetime (caso venha como string)
    if isinstance(transacao_dict.get("transacao_data"), str):
        transacao_dict["transacao_data"] = datetime.fromisoformat(transacao_dict["transacao_data"])
    
    # Extrair features da data
    data = transacao_dict["transacao_data"]
    transacao_dict["ano"] = data.year
    transacao_dict["mes"] = data.month
    transacao_dict["dia"] = data.day
    transacao_dict["hora"] = data.hour
    transacao_dict["dia_da_semana"] = data.weekday()  # 0=segunda, 6=domingo
    transacao_dict["fim_de_semana"] = 1 if data.weekday() >= 5 else 0
    
    # Remover o campo original de data (se o modelo não usar timestamp bruto)
    transacao_dict.pop("transacao_data", None)
    
    return transacao_dict
