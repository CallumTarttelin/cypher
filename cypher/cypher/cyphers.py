from abc import ABC, abstractmethod
from importlib import import_module
from string import ascii_lowercase as ALPHABET
from typing import Any, Dict, Callable


def validate(initial: str, answer: str, cypher: str, *args) -> bool:
    cypher = getattr(import_module(f'cypher.cyphers'), cypher)(*args)
    return cypher.decypher(initial) == answer


class Cypher(ABC):
    @abstractmethod
    def encypher(self, text: str) -> str:
        pass

    @abstractmethod
    def decypher(self, text: str) -> str:
        pass


class Caesar(Cypher):
    def __init__(self, shift: int):
        self.shift = shift

    def encypher(self, text: str) -> str:
        def inner(c: str) -> str:
            index = (ALPHABET.index(c) + self.shift) % 26
            return ALPHABET[index]

        return ''.join(map(inner, text))

    def decypher(self, text: str) -> str:
        def inner(c: str) -> str:
            index = (ALPHABET.index(c) - self.shift) % 26
            return ALPHABET[index]

        return ''.join(map(inner, text))


def caesar(text: str, shift: int) -> str:
    def inner(c: str) -> str:
        index = (ALPHABET.index(c) + shift) % 26
        return ALPHABET[index]

    return ''.join(map(inner, text))


CYPHERS: Dict[str, Callable[[str, Any], str]] = {
    "caesar": caesar
}
