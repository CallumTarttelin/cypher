from .cypher import Cypher


class Caesar(Cypher):
    def __init__(self, shift: int):
        self.shift = shift

    def encypher(self, text: str) -> str:
        pass

    def decypher(self, text: str) -> str:
        pass
