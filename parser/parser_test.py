import parser

import pytest


def test_tokenize_simple_expression():
    tokens = parser.tokenize("1 + 1")
    assert len(tokens) == 4
    assert tokens[0].token_type == parser.TokenType.NUMBER
    assert tokens[0].value == 1
    assert tokens[1].token_type == parser.TokenType.PLUS
    assert tokens[2].token_type == parser.TokenType.NUMBER
    assert tokens[2].value == 1
    assert tokens[3].token_type == parser.TokenType.EOE


def test_tokenize_complex_expression():
    tokens = parser.tokenize("(1 + 2) * 3 - 4 / 5")
    assert len(tokens) == 12


def test_parse_simple_expression():
    tokens = parser.tokenize("1 + 1")

    assert parser.Parser(tokens).parse() == 2


def test_evaluate_simple_expression():
    assert parser.evaluate("1 + 1") == 2


def test_evaluate_complex_expression():
    assert parser.evaluate("(1 + 2) * 3 - 4 / 2") == 7.0


def test_cannot_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        parser.evaluate("1 / 0")


def test_parens_precedence():
    assert parser.evaluate("1 + 2 * 3") == 7
    assert parser.evaluate("(1 + 2) * 3") == 9
