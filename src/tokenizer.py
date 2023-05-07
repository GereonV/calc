from collections.abc import Callable
from dataclasses import dataclass
from tokens import Token, TokenType
from typing import Self

@dataclass(frozen=True, slots=True)
class TokenError(Exception):
    text: str
    pos: int

class Tokenizer:
    __slots__ = "_text", "_pos"

    def __init__(self, text: str):
        self._text = text
        self._pos = 0

    def _skip_while(self, pred: Callable[[str], bool]):
        while self._pos < len(self._text) and pred(self._text[self._pos]):
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
            if self._text.startswith(s, self._pos):
                start = self._pos
                self._pos += len(s)
                return Token(t, None, start)

    def _identifier(self) -> Token | None:
        start = self._pos
        self._skip_while(lambda c: c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")
        return None if self._pos == start else Token(TokenType.ID, self._text[start:self._pos], start)

    # TODO extend syntax
    def _literal(self) -> Token | None:
        start = self._pos
        if (c := self._text[self._pos]).isdigit():
            self._pos += 1
            self._skip_while(lambda c: c.isdigit())
            if self._pos == len(self._text) or self._text[self._pos] != ".":
                return Token(TokenType.INT, int(self._text[start:self._pos]), start)
        elif c != ".":
            return None
        self._pos += 1
        self._skip_while(lambda c: c.isdigit())
        return Token(TokenType.FLOAT, float(self._text[start:self._pos]), start)

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Token:
        self._skip_while(lambda c: c == " ")
        if self._pos == len(self._text):
            raise StopIteration
        funcs = (
            self._simple_token,
            self._identifier,
            self._literal,
        )
        for f in funcs:
            if (t := f()) is not None:
                return t
        raise TokenError(self._text, self._pos)
