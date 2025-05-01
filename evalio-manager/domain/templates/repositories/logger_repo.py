from abc import ABC, abstractmethod

class LoggerInterface(ABC):
    @abstractmethod
    def info(self, message: str): pass

    @abstractmethod
    def error(self, message: str): pass

    @abstractmethod
    def warning(self, message: str): pass

    @abstractmethod
    def debug(self, message: str): pass