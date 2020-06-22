from abc import ABC, abstractmethod

from importlib import import_module

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


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

        return ''.join(list(map(inner, text)))

    def decypher(self, text: str) -> str:
        def inner(c: str) -> str:
            index = (ALPHABET.index(c) - self.shift) % 26
            return ALPHABET[index]

        return ''.join(list(map(inner, text)))
