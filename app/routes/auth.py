from fastapi import APIRouter, HTTPException
from app.db.database import db
from app.schemas.auth_schema import LoginInput
from app.utils.auth_utils import verificar_senha, gerar_token