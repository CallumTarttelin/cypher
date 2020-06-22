from abc import ABC, abstractmethod


class Cypher(ABC):
    @abstractmethod
    def encypher(self, text: str) -> str:
        pass

    @abstractmethod
    def decypher(self, text: str) -> str:
        pass
