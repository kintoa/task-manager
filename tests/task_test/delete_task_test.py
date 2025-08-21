import pytest
import uuid
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from src.main import app
from ..services import MockDb, make_task, mock_session


client = TestClient(app)


@pytest.mark.asyncio
async def test_delete_task_success(mock_session: mock_session):
    example_task = make_task()
    mock_session.execute.return_value = MockDb(example_task)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    response = client.delete(f"/api/v1/task/{example_task.uuid}")
    assert response.status_code == 200
    assert response.json() == {"message": "Запись успешно удалена"}


@pytest.mark.asyncio
async def test_delete_task_not_found(mock_session: mock_session):
    mock_session.execute.return_value = MockDb(None)

    response = client.delete(f"/api/v1/task/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Запись не найдена"}
