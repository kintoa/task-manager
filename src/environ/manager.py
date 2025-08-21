import json
import os
from typing import Any


class EnvManager:
    @classmethod
    def get_str(cls, value: str, default: str) -> str:
        """
        Метод преобразования энв в str
        """
        return os.getenv(value, default)

    @classmethod
    def get_int(cls, value: str, default: int) -> int:
        """
        Метод преобразования энв в int
        """
        result = os.getenv(value, None)

        if result is None:
            return default

        return int(result)

    @classmethod
    def get_bool(cls, value: str, default: bool) -> bool:
        """
        Метод преобразования энв в bool
        """
        result = os.getenv(value, None)

        if result is None:
            return default

        return result.lower() == "true"

    @classmethod
    def get_list(cls, value: str, default: list[Any]) -> list[Any]:
        """
        Метод преобразования энв в list[str, int]

        """
        str_env = os.getenv(value, None)

        if str_env is None:
            return default or []
        return [item.strip() for item in str_env.split(",")]

    @classmethod
    def get_dict(cls, value: str, default: dict[Any, Any]) -> dict[Any, Any]:
        """
        Метод преобразования энв в dict[str, str | int]

        """
        str_env = os.getenv(value, None)

        if str_env is None:
            return default

        return json.loads(str_env)
