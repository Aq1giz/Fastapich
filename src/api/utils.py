from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
import jwt
import bcrypt


SECRET_KEY = "very-very-seret-key"


def create_jwt_token(
    token_payload: dict,
    algorithm: str = "HS256",
    expire_mins: Annotated[Optional[int], "Time in minutes"] = 30,
    secret_key: str = SECRET_KEY    
) -> str | bytes:
    now = datetime.now(timezone.utc)
    token_payload["exp"] = now + timedelta(minutes=expire_mins)
    token_payload["iat"] = now
    token = jwt.encode(
        payload=token_payload,
        algorithm=algorithm,   
        key=secret_key,
    )
    return token


def decode_jwt_token(
    token: str | bytes,
    algorithms=["HS256"],
    secret_key=SECRET_KEY
) -> dict:
    jwt_data = jwt.decode(
        jwt=token,
        algorithms=algorithms,
        key=secret_key,
    )
    return jwt_data


def get_hashed_password_and_salt(
    password: str,
) -> tuple[bytes, bytes]:
    salt = bcrypt.gensalt()
    byted_password = bytes(password.encode("utf-8"))
    hashed_password = bcrypt.hashpw(byted_password, salt)
    return hashed_password, salt


def validate_password(
    auth_password: bytes,
    hash_salt: bytes,
    password_from_db: bytes,
) -> bool:
    hashed_auth_password = bcrypt.hashpw(auth_password, hash_salt)
    print(type(password_from_db), type(hashed_auth_password))
    return bcrypt.checkpw(password_from_db, hashed_auth_password)