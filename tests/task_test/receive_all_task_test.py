import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from src.main import app
from src.task_manager.schemas import TaskResponseSchema
from ..services import make_task, mock_session

client = TestClient(app)


@pytest.mark.asyncio
async def test_receive_all_tasks_success(mock_session: mock_session):
    task1 = make_task(id=1, title="Task 1")
    task2 = make_task(id=2, title="Task 2")

    # Создаём мок результата для execute()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [task1, task2]

    mock_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_result

    response = client.get("/api/v1/task/all")
    assert response.status_code == 200

    expected = [
        TaskResponseSchema.model_validate(task1).model_dump(),
        TaskResponseSchema.model_validate(task2).model_dump(),
    ]
    assert response.json() == expected


@pytest.mark.asyncio
async def test_receive_all_tasks_empty(mock_session: mock_session):
    # Создаём мок результата для execute()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []

    mock_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_result

    response = client.get("/api/v1/task/all")
    assert response.status_code == 404
    assert response.json() == {"detail": "В базе данных нет задач"}
