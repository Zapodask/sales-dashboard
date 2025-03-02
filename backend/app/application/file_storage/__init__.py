from abc import ABC, abstractmethod

from app.application.schemas.image_file import File


class BaseFileStorage(ABC):
    @abstractmethod
    async def put(self, key: str, file: File) -> str:
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass
