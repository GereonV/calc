from tokens import Token, tokenize, TokenType

def tokens() -> str:
    a = Token(TokenType.ID, "A")
    eq = Token(TokenType.EQ)
    mult = Token(TokenType.MULT)
    minus = Token(TokenType.MINUS)
    exp = Token(TokenType.EXP)
    lit = lambda x: Token(TokenType.LIT, x)
    first_test = [a, eq, lit("5"), mult, lit("3"), minus, lit("1")]
    tests = [
        ("A=5*3-1", first_test),
        ("  A = 5  * 3-  1", first_test),
        ("A= 5* 3 -1  ", first_test),
        ("5***2", [lit("5"), exp, mult, lit("2")]),
        ("5**2", [lit("5"), exp, lit("2")]),
        ("5.", None),
        ("  5.", None),
        ("5.  ", None),
        ("  5.  a", None),
        ("a  5.  ", None),
        ("b  .28437  a", None),
    ]
    for i, (s, l) in enumerate(tests):
        try:
            t = tokenize(s)
            if t == l:
                continue
            return f"failed at {s!r}\nexpected: {l}\nactual:   {t}"
        except Exception as e:
            return f"raised exception {e!r} at {s!r}"
    return "passed"

def main():
    test = lambda n, t: print(f"{n}: {t()}")
    test("Tokens", tokens)

if __name__ == "__main__":
    main()
