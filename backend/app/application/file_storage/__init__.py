from abc import ABC, abstractmethod


class BaseFileStorage(ABC):
    @abstractmethod
    async def put(self, key: str, value: bytes) -> str:
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass
