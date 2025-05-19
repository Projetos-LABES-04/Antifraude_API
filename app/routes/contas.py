from fastapi import APIRouter , HTTPException
from app.db.database import db
from app.schemas.conta_schema import ContaResumo

router = APIRouter()

@router.get("/contas/analise",response_model=list[ContaResumo])
async def listar_resumo_contas():
    try:
        