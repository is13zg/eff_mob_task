from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from config import settings

crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pass(plain: str) -> str:
    return crypto_context.hash(plain)


def check_pass(plain: str, hashed_pass: str) -> bool:
    return crypto_context.verify(plain, hashed_pass)


def gen_token(user_id: int) -> str:
    now = datetime.now()
    payload = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    print("=====", token , "=========")
    return token


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
