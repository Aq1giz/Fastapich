from fastapi import FastAPI
import uvicorn

app = FastAPI()

async def main():
    create_tables_task = asyncio.create_task(create_tables())
    await create_tables_task
    add_all_users_task = asyncio.create_task(add_all_users_db(
            usernames=["Misha", "Leva", "Nekit", "Ivan", "Grisha"],
            passwords=["qwerty123", "123432111", "34596382", "fsjiedof", "324dfd32"]))
    update_user_task = asyncio.create_task(update_user_db(user_id=3, new_username="Fsflajskf"))
    await add_all_users_task
    await update_user_task

    get_all_users_task = asyncio.create_task(get_users_pagination_db())
    all_users = await get_all_users_task
    print(all_users)