from __future__ import annotations
from dataclasses import dataclass
from enum import auto, Enum

class Operation(Enum):
    ADD  = auto()
    SUB  = auto()
    MULT = auto()
    DIV  = auto()
    IDIV = auto()
    NEG  = auto()
    POW  = auto()

class InstructionType(Enum):
    LOAD      = auto() # str
    STORE     = auto() # str
    PARAM     = auto() # int
    CALL      = auto() # int
    OPERATION = auto() # Operation
    INT       = auto() # int
    FLOAT     = auto() # float
    FUNCTION  = auto() # tuple[int, list[Instruction]]

@dataclass(frozen=True, slots=True)
class Instruction:
    type: InstructionType
    argument: str | int | float | Operation | tuple[int, list[Instruction]]

    def __repr__(self) -> str:
        arg = self.argument
        arg = arg.name if self.type is InstructionType.OPERATION else repr(arg)
        return f"Instruction({self.type}, {arg})"
