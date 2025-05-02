from abc import ABC, abstractmethod

class EventPublisher(ABC):
    @abstractmethod
    async def publish(self, subject: str, data: dict): pass