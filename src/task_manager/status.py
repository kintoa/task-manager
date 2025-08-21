from enum import Enum


class TaskStatus(Enum):
    CREATE = "CREATE"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
