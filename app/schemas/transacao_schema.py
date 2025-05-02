from pydantic import BaseModel, Field
from typing import Literal,Optional
from uuid import UUID
from datetime import datetime

class Transacao(BaseModel):
    _id: Optional[str] = None 
    transacao_id: str  
    cliente_id: int 
    conta_id: str  
    conta_destino_id: str  
    mesma_titularidade: bool 
    transacao_data: datetime  
    transacao_valor: float = Field(gt=0, description="O valor da transação deve ser maior que zero.")  # Validando que o valor é positivo
    transacao_tipo: Literal["pix", "boleto", "cartao", "transferencia"]  # Tipos de transação permitidos

    class Config:
        # Garantir que o UUID seja convertido para string e que as datas sejam formatadas corretamente
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
        }
