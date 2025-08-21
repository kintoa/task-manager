import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.task_manager.status import TaskStatus
from src.task_manager.schemas import TaskResponseSchema
from ..services import make_task, mock_session
import uuid

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_task_success(mock_session: mock_session):
    test_data = {
        "uuid": str(uuid.uuid4()),
        "title": "Test Task",
        "description": "Some description",
        "status": TaskStatus.CREATE.value,
    }

    fake_task = make_task(**test_data)

    # настраиваем мок для add/commit/refresh
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    async def fake_refresh(obj):
        obj.id = 1
        return obj

    mock_session.refresh = AsyncMock(side_effect=fake_refresh)

    response = client.post("/api/v1/task", json=test_data)
    assert response.status_code == 200
    assert response.json() == TaskResponseSchema.model_validate(fake_task).model_dump()


@pytest.mark.asyncio
async def test_create_task_commit_error(mock_session: mock_session):
    test_data = {
        "uuid": str(uuid.uuid4()),
        "title": "Broken Task",
        "description": "Should fail",
        "status": TaskStatus.CREATE.value,
    }

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock(side_effect=Exception("DB error"))
    mock_session.refresh = AsyncMock()

    response = client.post("/api/v1/task", json=test_data)
    assert response.status_code == 500
    assert response.json() == {"detail": "Ошибка сервера"}
