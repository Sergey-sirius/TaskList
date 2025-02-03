from pydantic import BaseModel, ConfigDict


class STaskAdd(BaseModel):
    name: str
    description: str | None = None


# наследуемся и добавляем id
class STask(STaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


# схема которая возвращает id от функции add_task
class STaskId(BaseModel):
    id: int