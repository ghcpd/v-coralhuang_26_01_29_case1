from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, List, Optional, Sequence, Union

import dialects_clean as dialects
from snowflake_clean import Dialect


class TokenType(Enum):
    COMMENT = auto()
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    OPERATOR = auto()
    STAR = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    text: str


@dataclass(frozen=True)
class Expression:
    pass


@dataclass(frozen=True)
class Literal(Expression):
    value: str


@dataclass(frozen=True)
class Star(Expression):
    pass


@dataclass(frozen=True)
class Select(Expression):
    expressions: List[Expression]


class Tokenizer:
    def __init__(self, dialect: Dialect) -> None:
        self.dialect = dialect

    def tokenize(self, sql: str) -> List[Token]:
        tokens: List[Token] = []
        i = 0
        length = len(sql)
        single_line = sorted(self.dialect.SINGLE_LINE_COMMENTS, key=len, reverse=True)
        block_comments = self.dialect.BLOCK_COMMENT_DELIMITERS

        while i < length:
            ch = sql[i]

            if ch.isspace():
                i += 1
                continue

            if sql.startswith("{#", i):
                end = sql.find("#}", i + 2)
                end_index = (end + 2) if end != -1 else length
                tokens.append(Token(TokenType.COMMENT, sql[i:end_index]))
                i = end_index
                continue

            matched = False
            for start, end in block_comments:
                if sql.startswith(start, i):
                    end_pos = sql.find(end, i + len(start))
                    end_index = (end_pos + len(end)) if end_pos != -1 else length
                    tokens.append(Token(TokenType.COMMENT, sql[i:end_index]))
                    i = end_index
                    matched = True
                    break
            if matched:
                continue

            for prefix in single_line:
                if sql.startswith(prefix, i):
                    end_pos = sql.find("\n", i + len(prefix))
                    end_index = end_pos if end_pos != -1 else length
                    tokens.append(Token(TokenType.COMMENT, sql[i:end_index]))
                    i = end_index
                    matched = True
                    break
            if matched:
                continue

            if sql.startswith("//", i):
                tokens.append(Token(TokenType.OPERATOR, "//"))
                i += 2
                continue

            if ch.isdigit():
                start = i
                i += 1
                while i < length and sql[i].isdigit():
                    i += 1
                tokens.append(Token(TokenType.NUMBER, sql[start:i]))
                continue

            if ch.isalpha() or ch == "_":
                start = i
                i += 1
                while i < length and (sql[i].isalnum() or sql[i] == "_"):
                    i += 1
                text = sql[start:i]
                if text.upper() == "SELECT":
                    tokens.append(Token(TokenType.KEYWORD, text.upper()))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, text))
                continue

            if ch == "*":
                tokens.append(Token(TokenType.STAR, ch))
                i += 1
                continue

            if ch in "+-/*":
                tokens.append(Token(TokenType.OPERATOR, ch))
                i += 1
                continue

            raise ValueError(f"Unexpected character: {ch}")

        return tokens


def _resolve_dialect(read: Optional[Union[str, Dialect, type]]) -> Dialect:
    if read is None:
        return dialects.Ansi()
    if isinstance(read, Dialect):
        return read
    if isinstance(read, str):
        name = read.lower()
        if name == "snowflake":
            return dialects.Snowflake()
        if name in {"ansi", "default"}:
            return dialects.Ansi()
        raise ValueError(f"Unknown dialect: {read}")
    if isinstance(read, type) and issubclass(read, Dialect):
        return read()
    raise TypeError("Invalid dialect for read")


def tokenize(sql: str, read: Optional[Union[str, Dialect, type]] = None) -> List[Token]:
    dialect = _resolve_dialect(read)
    return Tokenizer(dialect).tokenize(sql)


def parse_one(sql: str, read: Optional[Union[str, Dialect, type]] = None) -> Select:
    dialect = _resolve_dialect(read)
    tokens = Tokenizer(dialect).tokenize(sql)
    non_comment = [token for token in tokens if token.type != TokenType.COMMENT]

    if not non_comment:
        raise ValueError("Empty SQL")

    if non_comment[0].type != TokenType.KEYWORD or non_comment[0].text != "SELECT":
        raise ValueError("Only SELECT statements are supported")

    if len(non_comment) < 2:
        raise ValueError("SELECT requires an expression")

    expr_token = non_comment[1]
    if expr_token.type == TokenType.NUMBER:
        expression: Expression = Literal(expr_token.text)
    elif expr_token.type == TokenType.STAR:
        expression = Star()
    else:
        raise ValueError("Unsupported SELECT expression")

    if len(non_comment) > 2:
        raise ValueError("Unexpected tokens after SELECT expression")

    return Select(expressions=[expression])
