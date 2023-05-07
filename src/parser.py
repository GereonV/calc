from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from node import Node, NodeType
from tokens import Token, TokenType

@dataclass(frozen=True, slots=True)
class ParserError(Exception):
    expected: tuple[TokenType]
    actual: Token

class _Parser:
    __slots__ = "_tokens", "_next"

    def __init__(self, tokens: Iterator[Token]):
        self._tokens = tokens
        self._advance()

    def _advance(self):
        try:
            self._next = next(self._tokens)
        except StopIteration:
            self._next = None

    def _next_type_is(self, type: TokenType):
        return self._next is not None and self._next.type == type

    def _stmnt(self) -> Node:
        first = self._sum()
        if first.type != NodeType.IDENTIFIER or not self._next_type_is(TokenType.EQ):
            return first
        self._advance()
        rhs = self._sum()
        return Node(NodeType.ASSIGNMENT, (first.data, rhs))

    def _sum(self) -> Node:
        lhs = self._prod()
        while self._next is not None:
            match self._next.type:
                case TokenType.PLUS:  nt = NodeType.ADDITION
                case TokenType.MINUS: nt = NodeType.SUBTRACTION
                case _: break
            self._advance()
            rhs = self._prod()
            lhs = Node(nt, (lhs, rhs))
        return lhs

    def _prod(self) -> Node:
        lhs = self._neg()
        while self._next is not None:
            match self._next.type:
                case TokenType.MULT: nt = NodeType.MULTIPLICATION
                case TokenType.DIV:  nt = NodeType.DIVISION
                case TokenType.IDIV: nt = NodeType.IDIVISION
                case _: break
            self._advance()
            rhs = self._neg()
            lhs = Node(nt, (lhs, rhs))
        return lhs

    def _neg(self) -> Node:
        count = 0
        while self._next_type_is(TokenType.MINUS):
            count += 1
            self._advance()
        node = self._pow()
        for _ in range(count):
            node = Node(NodeType.NEGATION, node)
        return node

    def _pow(self) -> Node:
        stack = [self._val()]
        while self._next_type_is(TokenType.EXP):
            self._advance()
            stack.append(self._neg())
        rhs = stack.pop()
        while stack:
            lhs = stack.pop()
            rhs = Node(NodeType.POWER, (lhs, rhs))
        return rhs

    def _val(self) -> Node:
        EXPECTED = TokenType.ID, TokenType.INT, TokenType.FLOAT, TokenType.LPAR, TokenType.MINUS
        if self._next is None:
            raise ParserError(EXPECTED, None)
        match self._next.type:
            case TokenType.INT:
                node = Node(NodeType.INT, self._next.value)
            case TokenType.FLOAT:
                node = Node(NodeType.FLOAT, self._next.value)
            case TokenType.LPAR:
                self._advance()
                node = self._sum()
                if not self._next_type_is(TokenType.RPAR):
                    raise ParserError((TokenType.RPAR,), self._next)
            case TokenType.ID:
                id = self._next.value
                self._advance()
                if not self._next_type_is(TokenType.LPAR):
                    return Node(NodeType.IDENTIFIER, id)
                self._advance()
                params = [self._sum()]
                while self._next_type_is(TokenType.COMMA):
                    self._advance()
                    params.append(self._sum())
                if not self._next_type_is(TokenType.RPAR):
                    raise ParserError((TokenType.COMMA, TokenType.RPAR), self._next)
                node = Node(NodeType.CALL, (id, *params))
            case _: raise ParserError(EXPECTED, current)
        self._advance()
        return node

def parse(tokens: Iterable[Token]) -> Node:
    return _Parser(iter(tokens))._stmnt()
