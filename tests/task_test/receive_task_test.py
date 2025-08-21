import pytest
import uuid
from fastapi.testclient import TestClient

from src.main import app
from src.task_manager.schemas import TaskResponseSchema
from ..services import MockDb, make_task, mock_session

client = TestClient(app)


@pytest.mark.asyncio
async def test_receive_last_record_no_task(mock_session: mock_session):
    mock_session.execute.return_value = MockDb(None)

    response = client.get("/api/v1/task")
    assert response.status_code == 404
    assert response.json() == {"detail": "В базе данных нет задач"}


@pytest.mark.asyncio
async def test_receive_last_record(mock_session: mock_session):
    example_last_record = make_task(id=10)
    mock_session.execute.return_value = MockDb(example_last_record)

    response = client.get("/api/v1/task")
    assert response.status_code == 200
    assert (
        response.json()
        == TaskResponseSchema.model_validate(example_last_record).model_dump()
    )


@pytest.mark.asyncio
async def test_receive_record_by_uuid(mock_session: mock_session):
    example_last_record = make_task(id=10)
    mock_session.execute.return_value = MockDb(example_last_record)

    response = client.get(f"/api/v1/task?uuid={example_last_record.uuid}")
    assert response.status_code == 200
    assert (
        response.json()
        == TaskResponseSchema.model_validate(example_last_record).model_dump()
    )


@pytest.mark.asyncio
async def test_receive_record_by_wrong_uuid(mock_session: mock_session):
    mock_session.execute.return_value = MockDb(None)

    response = client.get(f"/api/v1/task?uuid={uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Не найдена запись в бд"}
