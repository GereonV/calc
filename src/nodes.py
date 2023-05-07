from __future__ import annotations
from dataclasses import dataclass
from enum import auto, Enum

class NodeType(Enum):
    ASSIGNMENT     = auto() # tuple[str, Node]
    DEFINITION     = auto() # tuple[str, tuple[str, ...], Node]
    ADDITION       = auto() # tuple[Node, Node]
    SUBTRACTION    = auto() # tuple[Node, Node]
    MULTIPLICATION = auto() # tuple[Node, Node]
    DIVISION       = auto() # tuple[Node, Node]
    IDIVISION      = auto() # tuple[Node, Node]
    NEGATION       = auto() # Node
    POWER          = auto() # tuple[Node, Node]
    IDENTIFIER     = auto() # str
    CALL           = auto() # tuple[str, tuple[Node, ...]]
    INT            = auto() # int
    FLOAT          = auto() # float

@dataclass(frozen=True, slots=True)
class Node:
    type: NodeType
    data: str | int | float | Node | tuple[str, Node] | tuple[str, tuple[str, ...], Node] | tuple[str, tuple[Node, ...]] | tuple[Node, Node]

    def __str__(self) -> str:
        data = self.data
        match self.type:
            case NodeType.ASSIGNMENT: return f"{data[0]}={data[1]}"
            case NodeType.DEFINITION: return f"{data[0]}({','.join(data[1])})={data[2]}"
            case NodeType.ADDITION: return f"({data[0]})+({data[1]})"
            case NodeType.SUBTRACTION: return f"({data[0]})-({data[1]})"
            case NodeType.MULTIPLICATION: return f"({data[0]})*({data[1]})"
            case NodeType.DIVISION: return f"({data[0]})/({data[1]})"
            case NodeType.IDIVISION: return f"({data[0]})//({data[1]})"
            case NodeType.NEGATION: return f"-({data})"
            case NodeType.POWER: return f"({data[0]})**({data[1]})"
            case NodeType.CALL: return f"{data[0]}({','.join(map(str, data[1]))})"
            case NodeType.IDENTIFIER | NodeType.INT | NodeType.FLOAT: return str(data)
            case _: raise TypeError

    def __repr__(self) -> str:
        return f"Node({self.type.name}, {self.data!r})"
