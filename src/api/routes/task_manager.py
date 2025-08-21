from fastapi import APIRouter
from src.task_manager.schemas import (
    TaskSchema,
    TaskUpdateInputSchema,
    TaskResponseSchema,
)
from fastapi import HTTPException
from starlette.responses import JSONResponse
from src.core.deps import SessionDep
from sqlmodel import select, desc
from src.task_manager.models import Task
from fastapi import Path
from typing import Optional
from fastapi import Query

router = APIRouter()


@router.get("", response_model=TaskResponseSchema)
async def receive_task(
    session: SessionDep,
    uuid: Optional[str] = Query(None, description="UUID задачи"),
):
    """Получение задачи по uuid/новой задачи

    Args:
        title (str): query параметр - uuid задачи
        по которому будет производиться поиск в бд

    Returns:
        TaskResponseSchema | JSONResponse: Объект задачи найденной по параметру
        или последней созданной | Ошибку
    """

    # Обработка случая без передачи параметра (вывод свежей записи)
    if not uuid:
        last_record = select(Task).order_by(desc(Task.id)).limit(1)
        result = await session.execute(last_record)
        print(result)
        last_record = result.scalar_one_or_none()
        if not last_record:
            raise HTTPException(status_code=404, detail="В базе данных нет задач")

        return TaskResponseSchema.model_validate(last_record)

    # Получение записи из бд по uuid
    record = select(Task).where(Task.uuid == uuid)
    result = await session.execute(record)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail="Не найдена запись в бд")

    return TaskResponseSchema.model_validate(record)


@router.get("/all", response_model=list[TaskResponseSchema])
async def receive_all_tasks(
    session: SessionDep,
):
    """Получение всех записей из базы"""

    result = await session.execute(select(Task).order_by(Task.id))
    records = result.scalars().all()

    if not records:
        raise HTTPException(status_code=404, detail="В базе данных нет задач")

    return [TaskResponseSchema.model_validate(record) for record in records]


@router.post("", response_model=TaskResponseSchema)
async def create_task(input_data: TaskSchema, session: SessionDep):
    """Создание новой задачи

    Args:
        input_data (TaskSchema): Входня схема задача с полями

    Returns:
        TaskResponseSchema | JSONResponse: Новая запись | Ошибку
    """
    try:
        # Создание экземпляра модели
        new_record = Task(
            uuid=input_data.uuid,
            title=input_data.title,
            description=input_data.description,
            status=input_data.status.value,
        )

        # Добавление записи в бд
        session.add(new_record)
        print(new_record)

        # Коммитим транзакцию для сохранения изменений
        await session.commit()

        # Получаем новую запись с id
        await session.refresh(new_record)

        print(new_record)

        return TaskResponseSchema.model_validate(new_record)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка сервера")


@router.patch("/{uuid}", response_model=TaskResponseSchema)
async def update_task(
    input_data: TaskUpdateInputSchema,
    session: SessionDep,
    uuid: str = Path(..., description="UUID задачи"),
):
    """Обновление записи в бд"""

    # Получение объекта
    result = await session.execute(select(Task).where(Task.uuid == uuid))
    record = result.scalar_one_or_none()

    if record is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    # Обновляем только переданные поля
    update_data = input_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)

    # Зафиксировать изменения
    await session.commit()
    await session.refresh(record)

    return TaskResponseSchema.model_validate(record)


@router.delete("/{uuid}")
async def delete_task(
    session: SessionDep,
    uuid: str = Path(..., description="UUID задачи"),
) -> JSONResponse:
    """Удаление задачи по uuid

    Returns:
        JSONResponse: Сообщение об успешном удалении
    """
    # Получение объекта
    result = await session.execute(select(Task).where(Task.uuid == uuid))
    record = result.scalar_one_or_none()

    if record is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    # Удалить задачу
    await session.delete(record)
    await session.commit()

    return JSONResponse(content={"message": "Запись успешно удалена"})
