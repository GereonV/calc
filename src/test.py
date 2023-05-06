from tokens import Token, TokenType
from tokenizer import TokenError, Tokenizer

def tokenizer() -> str:
    a = Token(TokenType.ID, "A", None)
    eq = Token(TokenType.EQ, None, None)
    mult = Token(TokenType.MULT, None, None)
    minus = Token(TokenType.MINUS, None, None)
    exp = Token(TokenType.EXP, None, None)
    int = lambda x: Token(TokenType.INT, x, None)
    float = lambda x: Token(TokenType.FLOAT, x, None)
    first_test = [a, eq, int(5), mult, int(3), minus, int(1)]
    err = lambda s, p: (s, TokenError(s, p))
    tests = [
        ("A=5*3-1", first_test),
        ("  A = 5  * 3-  1", first_test),
        ("A= 5* 3 -1  ", first_test),
        ("5***2", [int(5), exp, mult, int(2)]),
        ("5**2", [int(5), exp, int(2)]),
        ("5.", [float(5)]),
        ("5.0", [float(5)]),
        ("  5.0  ", [float(5)]),
        ("  .5  ", [float(.5)]),
        (".0", [float(0)]),
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
    return "passed"

def main():
    test = lambda n, t: print(f"{n}: {t()}")
    test("Tokens", tokenizer)

if __name__ == "__main__":
    main()
