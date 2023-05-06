from dataclasses import dataclass
from enum import auto, Enum

class TokenType(Enum):
    ID    = auto()
    INT   = auto()
    FLOAT = auto()
    EQ    = auto()
    LPAR  = auto()
    RPAR  = auto()
    PLUS  = auto()
    MINUS = auto()
    EXP   = auto()
    MULT  = auto()
    IDIV  = auto()
    DIV   = auto()
    COMMA = auto()

@dataclass(frozen=True, slots=True)
class Token:
    type: TokenType
    value: str | int | float = None

    def __str__(self) -> str:
        return self.type.name if self.str is None else f"{self.type.name}={self.str!r}"

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.str!r})"
