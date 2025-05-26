from fastapi import APIRouter , HTTPException,Query
from app.db.database import db
from app.schemas.conta_schema import ContaResumo
from datetime import datetime, timedelta

router = APIRouter()

