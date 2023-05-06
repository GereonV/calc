from collections.abc import Callable
from dataclasses import dataclass
from tokens import Token, TokenType

@dataclass(frozen=True, slots=True)
class TokenError(Exception):
    text: str
    pos: int

class Tokenizer:
    __slots__ = "_str", "_pos"

    def __init__(self, s: str, /):
        self._str = s
        self._pos = 0

    def _skip_while(self, pred: Callable[[str], bool]):
        while self._pos < len(self._str) and pred(self._str[self._pos]):
            self._pos += 1

    def _simple_token(self) -> Token | None:
        mapping = (
            ("=",  TokenType.EQ),
            ("(",  TokenType.LPAR),
            (")",  TokenType.RPAR),
            ("+",  TokenType.PLUS),
            ("-",  TokenType.MINUS),
            ("**", TokenType.EXP),
            ("*",  TokenType.MULT),
            ("//", TokenType.IDIV),
            ("/",  TokenType.DIV),
            (",",  TokenType.COMMA),
        )
        for s, t in mapping:
            if self._str.startswith(s, self._pos):
                self._pos += len(s)
                return Token(t)

    def _identifier(self) -> Token | None:
        start = self._pos
        self._skip_while(lambda c: c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")
        return None if self._pos == start else Token(TokenType.ID, self._str[start:self._pos])

    # TODO extend syntax
    def _literal(self) -> Token | None:
        start = self._pos
        if (c := self._str[self._pos]).isdigit():
            self._pos += 1
            self._skip_while(lambda c: c.isdigit())
            if self._pos == len(self._str) or self._str[self._pos] != ".":
                return Token(TokenType.INT, int(self._str[start:self._pos]))
        elif c != ".":
            return None
        self._pos += 1
        self._skip_while(lambda c: c.isdigit())
        return Token(TokenType.FLOAT, float(self._str[start:self._pos]))

    def __iter__(self) -> 'Self':
        return self

    def __next__(self) -> Token | None:
        self._skip_while(lambda c: c == " ")
        if self._pos == len(self._str):
            raise StopIteration
        funcs = (
            self._simple_token,
            self._identifier,
            self._literal,
        )
        for f in funcs:
            if (t := f()) is not None:
                return t
        raise TokenError(self._str, self._pos)
