from sqlalchemy import select
from database import TaskOrm, new_session
from schemas import STask, STaskAdd


# Функция использует фабрику сессий new_session и модель TaskOrm, чтобы добавить в таблицу tasks новую строку
async def add_task(data: dict) -> int:
    async with new_session() as session:   # автоматически закрывать сессию при выходе из менеджера
        new_task = TaskOrm(**data)         # создает новую строку
        session.add(new_task)              # добавить новую строку в объект сессии
        await session.flush()              # отправляет в базу данных SQL запрос и получить значение столбца id
        await session.commit()             # коммитит изменения в базе данных, завершая транзакцию
        return new_task.id                 # вернуть id добавленой задачи


# получить список всех задач
async def get_tasks():
    async with new_session() as session:
        query = select(TaskOrm)
        result = await session.execute(query)
        task_models = result.scalars().all()    # итератор, нужно пройтись и выбрать все результаты.
        return task_models


class TaskRepository:
    @classmethod
    async def add_task(cls, task: STaskAdd) -> int:
        async with new_session() as session:
            data = task.model_dump()   # Pydantic-схема преобразует ее в словарь
            new_task = TaskOrm(**data)
            session.add(new_task)
            await session.flush()
            await session.commit()
            return new_task.id

    @classmethod
    async def get_tasks(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks = [STask.model_validate(task_model) for task_model in task_models]
            return tasks
