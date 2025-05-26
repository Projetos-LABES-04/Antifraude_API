from pydantic import BaseModel
from typing import List
from datetime import datetime

class AlertaRecente(BaseModel):
    mensagem: str
    timestamp: datetime

class DashboardResumo(BaseModel):
    total_transacoes: int
    transacoes_suspeitas: int
    fraudes_confirmadas: int
    valor_medio_suspeitas: float
