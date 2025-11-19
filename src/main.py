from fastapi import FastAPI, Response, HTTPException
from api.routers import crud, users
from api.database import database
from api.database import UsersORM
from api.utils import get_hashed_password_and_salt
from contextlib import asynccontextmanager
import bcrypt

import asyncio
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables_task = asyncio.create_task(database.create_tables())
    await create_tables_task

    password_list = []
    salt_list = []

    for password in ["qwerty123", "123432111", "34596382", "fsjiedof", "324dfd32"]:
        hashed_password, salt = get_hashed_password_and_salt(password)
        password_list.append(hashed_password)
        salt_list.append(salt)


    add_users_task = asyncio.create_task(database.add_all_users_db(
        usernames=["Misha", "Leva", "Nekit", "Ivan", "Grisha"],
        passwords=password_list,
        salt=salt_list,
    ))
    await add_users_task
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(crud.router)
app.include_router(users.router)


@app.get("/")
def default_endpoint(response: Response):
    return {
        "message": "OK",
        "status_code": response.status_code
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)