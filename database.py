from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# создаем асинхронное подключение, которое будет отвечать за отправку запросов в базу данных `engine`.
engine = create_async_engine("sqlite+aiosqlite:///tasks.db")

# После создания `engine`, мы дополнительно создаем фабрику сессий `new_session`.
new_session = async_sessionmaker(engine, expire_on_commit=False)


# Родительский класс
class Model(DeclarativeBase):
    pass


# создадим модель задач, наследованный
# Модель TaskOrm полностью описывает таблицу внутри базы данных, задает первичные и внешние ключи, индексы и т.д.
class TaskOrm(Model):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]


# функция создания таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


# функция удаления таблиц
async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
