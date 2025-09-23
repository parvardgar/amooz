from abc import ABC, abstractmethod
from typing import TypeVar, Type


T = TypeVar('T')


class BaseCommandHandler(ABC):
    @abstractmethod
    def handle(self, command: T):
        pass


class BaseQueryHandler(ABC):
    @abstractmethod
    def handle(self, query: T):
        pass


class Command:
    pass


class Query:
    pass