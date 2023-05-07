from collections.abc import Callable
from nodes import Node, NodeType
from parser import Parser, ParserError
from tokens import Token, TokenType
from tokenizer import TokenError, Tokenizer

def tokenizer() -> str | None:
    a = Token(TokenType.ID, "A", None)
    eq = Token(TokenType.EQ, None, None)
    mult = Token(TokenType.MULT, None, None)
    minus = Token(TokenType.MINUS, None, None)
    exp = Token(TokenType.EXP, None, None)
    lpar = Token(TokenType.LPAR, None, None)
    rpar = Token(TokenType.RPAR, None, None)
    div = Token(TokenType.DIV, None, None)
    idiv = Token(TokenType.IDIV, None, None)
    int = lambda x: Token(TokenType.INT, x, None)
    float = lambda x: Token(TokenType.FLOAT, x, None)
    foo = Token(TokenType.ID, "foo", None)
    comma = Token(TokenType.COMMA, None, None)
    first_test = [a, eq, int(5), mult, int(3), minus, int(1)]
    err = lambda s, p: (s, TokenError(s, p))
    tests = [
        ("A=5*3-1", first_test),
        ("  A = 5  * 3-  1", first_test),
        ("A= 5* 3 -1  ", first_test),
        ("5***2", [int(5), exp, mult, int(2)]),
        ("5**2", [int(5), exp, int(2)]),
        ("5///2", [int(5), idiv, div, int(2)]),
        ("5.", [float(5)]),
        ("5.0", [float(5)]),
        ("  5.0  ", [float(5)]),
        ("  .5  ", [float(.5)]),
        (".0", [float(0)]),
        ("(3.14)", [lpar, float(3.14), rpar]),
        ("foo(foo, A)", [foo, lpar, foo, comma, a, rpar]),
        err(" . ", 1),
        err(";", 0),
        err("abc;", 3),
    ]
    for s, e in tests:
        try:
            a = list(Tokenizer(s))
        except TokenError as err:
            a = err
        except Exception as ex:
            return f"raised exception {ex!r} at {s!r}"
        if a != e:
            return f"failed at {s!r}\nexpected: {e}\nactual:   {a}"

def parser() -> str | None:
    a = Token(TokenType.ID, "A", None)
    eq = Token(TokenType.EQ, None, None)
    mult = Token(TokenType.MULT, None, None)
    minus = Token(TokenType.MINUS, None, None)
    exp = Token(TokenType.EXP, None, None)
    lpar = Token(TokenType.LPAR, None, None)
    rpar = Token(TokenType.RPAR, None, None)
    int = lambda x: Token(TokenType.INT, x, None)
    float = lambda x: Token(TokenType.FLOAT, x, None)
    first_test = [a, eq, int(5), mult, int(3), minus, int(1)]
    err = lambda s, p: (s, TokenError(s, p))
    tests = [
        (first_test, Node(NodeType.ASSIGNMENT,(
            "A",
            Node(NodeType.SUBTRACTION, (
                Node(NodeType.MULTIPLICATION,(
                    Node(NodeType.INT, 5),
                    Node(NodeType.INT, 3)
                )),
                Node(NodeType.INT, 1)
            ))
        ))),
    ]

def test(name: str, function: Callable[[], str | None], errors: list[str]):
    result = function()
    if result is not None:
        errors.append(f"{name} {result}")
        status = "failed"
    else:
        status = "passed"
    print(f"Test {name}: {status}")

def main():
    tests = [
        ("Tokenizer", tokenizer),
        ("Parser", parser),
    ]
    errors = []
    for n, t in tests:
        test(n, t, errors)
    for e in errors:
        print(f"\n{e}")

if __name__ == "__main__":
    main()
