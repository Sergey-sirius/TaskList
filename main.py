import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import router as tasks_router


# функция которая будет создавать таблицу при запуске и удалять при выключении
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    # то что выполнится при выключении
    await delete_tables()
    print("База очищена")


# lifespan будет выполняться при старте
app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)


if __name__ == '__main__':
    #
    server_ip = '127.0.0.1'
    server_port = 8000
    # uvicorn.run("main:app", host=conf.get("server_ip"), port=conf.get("server_port"), reload=True)
    uvicorn.run("main:app", host=server_ip, port=server_port, reload=True)
