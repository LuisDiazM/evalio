from abc import ABC, abstractmethod

class EventPublisher(ABC):
    @abstractmethod
    async def publish(self, data: str, subject: str): pass