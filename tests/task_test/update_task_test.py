import pytest
import uuid
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from src.main import app
from src.task_manager.schemas import TaskResponseSchema
from ..services import MockDb, make_task, mock_session


client = TestClient(app)


@pytest.mark.asyncio
async def test_update_task_success(mock_session: mock_session):
    example_task = make_task()
    mock_session.execute.return_value = MockDb(example_task)
    mock_session.commit = AsyncMock()

    async def fake_refresh(obj):
        return obj

    mock_session.refresh = AsyncMock(side_effect=fake_refresh)

    update_data = {"title": "New title"}

    response = client.patch(f"/api/v1/task/{example_task.uuid}", json=update_data)
    assert response.status_code == 200

    # Проверяем, что объект обновился
    expected = TaskResponseSchema.model_validate(example_task).model_dump()
    expected["title"] = "New title"
    assert response.json() == expected


@pytest.mark.asyncio
async def test_update_task_not_found(mock_session: mock_session):
    mock_session.execute.return_value = MockDb(None)

    update_data = {"title": "Test"}

    response = client.patch(f"/api/v1/task/{uuid.uuid4()}", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Запись не найдена"}
