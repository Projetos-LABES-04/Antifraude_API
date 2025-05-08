from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.utils.auth_utils import criar_token