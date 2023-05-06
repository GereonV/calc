from dataclasses import dataclass
from enum import auto, Enum

"""
<stmnt>  ::= <id>=<sum>|<sum>
<sum>    ::= <prod>|<sum>+<prod>|<sum>-<prod>
<prod>   ::= <neg>|<prod>*<neg>|<prod>/<neg>|<prod>//<neg>
<neg>    ::= <pow>|-<neg>
<pow>    ::= <val>|<val>**<neg>
<val>    ::= <id>|<id>(<params>)|<lit>|(<sum>)
<params> ::= <sum>|<params>,<sum>
"""

class NodeType(Enum):
    ASSIGNMENT     = auto() # tuple[str, Node]
    ADDITION       = auto() # tuple[Node, Node]
    SUBTRACTION    = auto() # tuple[Node, Node]
    MULTIPLICATION = auto() # tuple[Node, Node]
    DIVISION       = auto() # tuple[Node, Node]
    IDIVISION      = auto() # tuple[Node, Node]
    NEGATION       = auto() # Node
    POWER          = auto() # tuple[Node, Node]
    IDENTIFIER     = auto() # str
    CALL           = auto() # tuple[str, Node, ...]
    INT            = auto() # int
    FLOAT          = auto() # float

@dataclass(frozen=True, slots=True)
class Node:
    type: NodeType
    data: None # I hate Python's type hints...
