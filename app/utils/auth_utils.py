from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta


SECRET_KEY = "chave_muito_segura"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60
