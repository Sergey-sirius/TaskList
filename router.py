from fastapi import APIRouter, Depends
from repository import TaskRepository
from schemas import STask, STaskAdd, STaskId

# Роутер — позволит создавать приложения с одним эндпоинтом не только в одном файле `main.py`
# структура проекта будет легко читаема
router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)


# для добавления одной задачи
# добавляем Depends для улучшения работы с документацией Api
# Появится понятная пометка для обязательного поля и его можно удобно заполнить в выделенной области
@router.post("")
async def add_task(task: STaskAdd = Depends()) -> STaskId:
    new_task_id = await TaskRepository.add_task(task)
    return {"id": new_task_id}


# получения всех
@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.get_tasks()
    return tasks
