from dataclasses import dataclass, field
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
    value: str | int | float | None
    pos: int = field(compare=False)

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value!r})"
