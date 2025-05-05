from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
from uuid import UUID
from datetime import datetime
import re

class Transacao(BaseModel):
    _id: Optional[str] = None 
    transacao_id: str = Field(..., min_length=10, max_length=50)
    cliente_id: int = Field(..., gt=0)
    conta_id: str = Field(..., min_length=5, max_length=20)
    conta_destino_id: str = Field(..., min_length=5, max_length=20)
    mesma_titularidade: bool 
    transacao_data: datetime  
    transacao_valor: float = Field(..., gt=0, le=1000000, description="O valor deve estar entre 0 e 1.000.000")
    transacao_tipo: Literal["pix", "boleto", "cartao", "transferencia"]
    
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
        }
