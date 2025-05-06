from fastapi import APIRouter, Query
from typing import List, Optional
from app.schemas.conta_schema import Conta
from app.services.conta_service import listar_contas

router = APIRouter()

@router.get("/contas", response_model=List[Conta])
def get_contas(status: Optional[str] = Query(None, description="Filtrar por status da conta")):
    return listar_contas(status=status)
