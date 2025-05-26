from pydantic import BaseModel
from datetime import datetime

class ContaResumo(BaseModel):
    conta_id:str
    cliente_id:int
    ultima_atividade:datetime
    valor_ultima:float
    status:str