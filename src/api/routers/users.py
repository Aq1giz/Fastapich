from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Form,
    status,
    Query,
)
from fastapi.responses import Response
import jwt

from .. import UsersPostSchema
from ..database import get_user_by_id
from ..database import add_user_db
from ..utils import create_jwt_token
from ..utils import get_hashed_password_and_salt
from ..utils import validate_password
import bcrypt


router = APIRouter(
    tags=["USRES"]
)
COOKIE_SESSION_ID = "auth-session"
COOKIE_USER_ID = "user_id"
SECRET_JWT_TOKEN = "very-very-secret-token(very)"


def validate_auth(
    username: str = Form(),
    password: str = Form(),
):
    pass


@router.post("/user-registration")
async def user_registration(
    user: UsersPostSchema,
    response: Response,
):
    hash_password, salt = get_hashed_password_and_salt(user.password)
    result = await add_user_db(
        username=user.username,
        password=hash_password,
        hash_salt=salt
    )
    payload={
        "sub": result.id,
        "username": result.username
    }
    token = create_jwt_token(payload)
    response.set_cookie(COOKIE_SESSION_ID, token)
    response.set_cookie(COOKIE_USER_ID, result.id)
    return result


@router.post("/user-login")
async def user_login(
    user: UsersPostSchema,
    response: Response,
    user_id: int = Query(ge=0),
):
    try: 
        result = await get_user_by_id(user_id)
        if validate_password(
            user.password,
            result.hash_salt,
            result.password
        ):
            payload={
                "sub": result.id,
                "username": result.username,
            }
            token = create_jwt_token(payload)
            response.set_cookie(COOKIE_SESSION_ID, token)
            response.set_cookie(COOKIE_USER_ID, result.id)
            return result
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password"
            )
    except ValueError as v:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(v)
        )
    

@router.get("/user-secret")
async def protected(
    response: Response,
    request: Request,
):
    token = request.cookies.get(COOKIE_SESSION_ID)
    payload = jwt.decode(token, algorithms=["HS256"])
    
    return payload