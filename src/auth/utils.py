from passlib.context import CryptContext
from datetime import datetime, timedelta
from uuid import uuid4
import jwt
import logging

from src.utils.config import settings


password_context = CryptContext(
    schemes=['bcrypt']
)


def get_password_hash(password: str) -> str:
    hash_string = password_context.hash(password)
    return hash_string


def verify_password(password: str, hash_string: str) -> bool:
    return password_context.verify(password, hash_string) 


def create_access_token(user_data: dict, expiry: timedelta = 3600, refresh: bool = False):
    payload = {
        "user": user_data,
        "exp": datetime.now() + timedelta(seconds=expiry),
        "jti": str(uuid4()),
        "refresh": refresh
    }
    
    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    
def decode_token(jwt_token: str):
    
    try:
        token_data = jwt.decode(
            jwt=jwt_token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.PyJWKError as jwt_e:
        logging.exception(jwt_e)
        return None