from fastapi import Fastapi
import uvicorn

app = Fastapi()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)