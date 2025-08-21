from src.task_manager.models import Task
from src.task_manager.status import TaskStatus
from unittest.mock import AsyncMock
from src.core.deps import get_async_session
from src.main import app
import pytest
import uuid


class MockDb:
    def __init__(self, value):
        self.mock_value = value

    def scalar_one_or_none(self):
        return self.mock_value

    def all(self):
        return self.mock_value


@pytest.fixture
def mock_session():
    mock_db = AsyncMock()
    app.dependency_overrides[get_async_session] = lambda: mock_db
    return mock_db


def make_task(**kwargs):
    return Task(
        id=kwargs.get("id", 1),
        uuid=kwargs.get("uuid", str(uuid.uuid4())),
        title=kwargs.get("title", "Test"),
        description=kwargs.get("description", "desc"),
        status=kwargs.get("status", TaskStatus.CREATE),
    )
