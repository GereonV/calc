from tokens import Token, TokenType

_ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
_SINGLE_CHAR = {
    "=": TokenType.EQ,
    "(": TokenType.LPAR,
    ")": TokenType.RPAR,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    ",": TokenType.COMMA,
}

def _identifier(s: str) -> tuple[str, str]:
    l = len(s)
    n = 1
    while n < l and s[n] in _ALPHA:
        n += 1
    return s[:n], s[n:]

def _literal(s: str) -> tuple[str, str]:
    l = len(s)
    n = 1
    def to_nondigit():
        nonlocal s, l, n
        while n < l and s[n].isdigit():
            n += 1
    to_nondigit()
    if n + 1 < l and s[n] == "." and s[n + 1].isdigit():
        n += 2
        to_nondigit()
    return s[:n], s[n:]

def tokenize(s: str) -> list[Token] | None:
    tokens = []
    while (s := s.lstrip()):
        v = None
        c = s[0]
        if (t := _SINGLE_CHAR.get(c)) is not None:
            s = s[1:]
        elif c in _ALPHA:
            v, s = _identifier(s)
            t = TokenType.ID
        elif c.isdigit():
            v, s = _literal(s)
            t = TokenType.LIT
        elif s.startswith("**"):
            s = s[2:]
            t = TokenType.EXP
        elif c == "*":
            s = s[1:]
            t = TokenType.MULT
        elif s.startswith("//"):
            s = s[2:]
            t = TokenType.IDIV
        elif c == "/":
            s = s[1:]
            t = TokenType.DIV
        else:
            return None
        tokens.append(Token(t, v))
    return tokens
