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
        current = self._next
        self._advance()
        match current.type:
            case TokenType.INT:   nt = NodeType.INT
            case TokenType.FLOAT: nt = NodeType.FLOAT
            case TokenType.ID:    nt = None if self._next_type_is(TokenType.LPAR) else NodeType.IDENTIFIER
            case _: raise ParserError(EXPECTED, current)
        if nt is not None:
            return Node(nt, current.value)
        self._advance()
        params = [self._sum()]
        EXPECTED = (*EXPECTED, TokenType.RPAR, TokenType.COMMA)
        while self._next is not None:
            if self._next.type == TokenType.RPAR:
                self._advance()
                return Node(NodeType.CALL, (current.value, *params))
            if self._next.type == TokenType.COMMA:
                self._advance()
                params.append(self._sum())
            else:
                break
        raise ParserError(EXPECTED, self._next)

def parse(tokens: Iterable[Token]) -> Node:
    return _Parser(iter(tokens))._stmnt()
