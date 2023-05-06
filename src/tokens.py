from dataclasses import dataclass
from enum import auto, IntEnum
from itertools import islice

ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

class TokenType(IntEnum):
    ID    = auto()
    LIT   = auto()
    EQ    = auto()
    LPAR  = auto()
    RPAR  = auto()
    PLUS  = auto()
    MINUS = auto()
    MULT  = auto()
    DIV   = auto()
    IDIV  = auto()
    COMMA = auto()
    EXP   = auto()

SINGLE_CHAR = {
    "=": TokenType.EQ,
    "(": TokenType.LPAR,
    ")": TokenType.RPAR,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    ",": TokenType.COMMA,
}

@dataclass
class Token:
    type: TokenType
    str: str = None

    def __str__(self) -> str:
        return self.type.name if self.str is None else f"{self.type.name}={self.str!r}"

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.str!r})"

def identifier(s: str) -> tuple[str, str]:
    l = len(s)
    n = 1
    while n < l and s[n] in ALPHA:
        n += 1
    return s[:n], s[n:]

def literal(s: str) -> tuple[str, str]:
    l = len(s)
    n = 1
    def to_nondigit():
        nonlocal s, l, n
        while n < l and s[n].isdigit():
            n += 1
    to_nondigit()
    if n + 1 < l and s[n] == "." and s[n + 1].isdigit():
        n += 2
        to_nondigit()
    return s[:n], s[n:]

def tokenize(s: str) -> list[Token] | None:
    tokens = []
    while (s := s.lstrip()):
        v = None
        c = s[0]
        if (t := SINGLE_CHAR.get(c)) is not None:
            s = s[1:]
        elif c in ALPHA:
            v, s = identifier(s)
            t = TokenType.ID
        elif c.isdigit():
            v, s = literal(s)
            t = TokenType.LIT
        elif s.startswith("**"):
            s = s[2:]
            t = TokenType.EXP
        elif c == "*":
            s = s[1:]
            t = TokenType.MULT
        elif s.startswith("//"):
            s = s[2:]
            t = TokenType.IDIV
        elif c == "/":
            s = s[1:]
            t = TokenType.DIV
        else:
            return None
        tokens.append(Token(t, v))
    return tokens
