from pydantic import BaseModel
from typing import Optional

class Conta(BaseModel):
    id: int
    nome: str
    status: str
