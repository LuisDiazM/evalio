from abc import ABC, abstractmethod

class EventSubscriber(ABC):
    @abstractmethod
    async def subscribe(self, subject: str, callback): pass
