from fastapi import APIRouter, Request, Query, HTTPException, status
from fastapi.responses import Response
import jwt

from .. import UsersPostSchema
from ..database import get_user_by_id
from ..database import add_user_db


router = APIRouter(
    tags=["USRES"]
)
COOKIE_SESSION_ID = "auth-session"
COOKIE_USER_ID = "user_id"
SECRET_JWT_TOKEN = "very-very-secret-token(very)"


@router.post("/user-registration")
async def user_registration(
    user: UsersPostSchema,
    response: Response,
):
    try:
        result = await add_user_db(
            username=user.username,
            password=user.password
        )
        token = jwt.encode(
            payload={
                "id": result.id,
                "username": result.username
            },
            key=SECRET_JWT_TOKEN,
            algorithm="HS256", # Но надо RS256
        )
        response.set_cookie(COOKIE_SESSION_ID, token)
        response.set_cookie(COOKIE_USER_ID, result.id)
        return result
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        )


@router.post("/user-login")
async def user_login(
    user: UsersPostSchema,
    response: Response,
    user_id: int = Query(ge=0),
):
    try: 
        result = await get_user_by_id(user_id)
        result = result[0]
        if user.username == result.username and user.password == result.password: # Сдлать через bcrypt
            token = jwt.encode(
                payload={
                    "id": result.id,
                    "username": result.username
                },
                key=SECRET_JWT_TOKEN,
                algorithm="HS256", # Но надо RS256
            )
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