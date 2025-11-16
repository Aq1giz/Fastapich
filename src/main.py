from fastapi import FastAPI, Response
from fastapi.security import 
from api.routers import crud
from api.database import database

import asyncio
import uvicorn

app = FastAPI()

app.include_router(crud.router)


@app.get("/")
def default_endpoint(response: Response):
    return {
        "message": "OK",
        "status_code": response.status_code
    }

async def main():
    create_tables_task = asyncio.create_task(database.create_tables())
    await create_tables_task
    add_all_users_task = asyncio.create_task(database.add_all_users_db(
            usernames=["Misha", "Leva", "Nekit", "Ivan", "Grisha"],
            passwords=["qwerty123", "123432111", "34596382", "fsjiedof", "324dfd32"]))
    update_user_task = asyncio.create_task(database.update_user_db(user_id=3, new_username="Fsflajskf"))
    await add_all_users_task
    await update_user_task

    get_all_users_task = asyncio.create_task(database.get_users_pagination_db())
    all_users = await get_all_users_task
    print(all_users)


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run("main:app", reload=True)