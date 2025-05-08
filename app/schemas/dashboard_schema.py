from pydantic import BaseModel
from typing import List
from datetime import datetime

class AlertaRecente(BaseModel):
    mensagem: str
    timestamp: datetime

class DashboardResumo(BaseModel):
    total_transacoes: int
    transacoes_suspeitas: int
    contas_investigadas: int
    fraudes_confirmadas: int
    alertas_recentes: List[AlertaRecente]
