import re

"""
expression     -> term ((PLUS | MINUS) term)*
term           -> factor ((MUL | DIV) factor)*
factor         -> NUMBER | LPAREN expression RPAREN
"""


class TokenType:
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOE = "EOE"  # end of expression


class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value


tokens_spec = [
    ("NUMBER", r"\d+(\.\d*)?"),
    ("PLUS", r"\+"),
    ("MINUS", r"\-"),
    ("MUL", r"\*"),
    ("DIV", r"\/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("EOE", r"\$"),
    ("SKIP", r"\s+"),
]


def tokenize(data):
    # groups by name
    spec = re.compile("|".join("(?P<%s>%s)" % pair for pair in tokens_spec))

    tokens = []

    for match in re.finditer(spec, data):
        token_type = match.lastgroup
        value = match.group(token_type)
        if token_type == "NUMBER":
            value = float(value)
            tokens.append(Token(token_type, value))
        elif token_type != "SKIP":
            tokens.append(Token(token_type))

    tokens.append(Token(TokenType.EOE))

    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.curr_token = next(self.tokens, None)
        self.next_token = next(self.tokens, None)

    def advance(self):
        self.curr_token = self.next_token
        self.next_token = next(self.tokens, None)

    def consume(self, token_type):
        if self.curr_token.token_type != token_type:
            raise Exception(
                f"Unexpected token {self.curr_token.type} at {self.curr_token.value}"
            )

        self.advance()

    def factor(self):
        token = self.curr_token
        if token.token_type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            return token.value

        if token.token_type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            result = self.expression()
            self.consume(TokenType.RPAREN)
            return result

        raise Exception(f"Unexpected factor {token.token_type}")

    def term(self):
        result = self.factor()

        while self.curr_token.token_type in (TokenType.MUL, TokenType.DIV):
            if self.curr_token.token_type == TokenType.MUL:
                self.consume(TokenType.MUL)
                result *= self.factor()
            if self.curr_token.token_type == TokenType.DIV:
                self.consume(TokenType.DIV)
                result /= self.factor()
        return result

    def expression(self):
        result = self.term()
        while self.curr_token.token_type in (TokenType.PLUS, TokenType.MINUS):
            if self.curr_token.token_type == TokenType.PLUS:
                self.consume(TokenType.PLUS)
                result += self.term()
            if self.curr_token.token_type == TokenType.MINUS:
                self.consume(TokenType.MINUS)
                result -= self.term()

        return result

    def parse(self):
        if not self.curr_token:
            return None
        return self.expression()


def evaluate(data):
    tokens = tokenize(data)
    return Parser(tokens).parse()
