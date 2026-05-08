"""
Urdu Custom Compiler - Parser (Recursive-Descent)
Converts tokens into an AST. No external libraries used.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union
from .lexer import Token, TokenType


# ── AST Nodes ──

@dataclass
class NumberNode:
    value: Union[int, float]

@dataclass
class StringNode:
    value: str

@dataclass
class BoolNode:
    value: bool

@dataclass
class VarNode:
    name: str

@dataclass
class BinOpNode:
    left: "ASTNode"
    op: str
    right: "ASTNode"

@dataclass
class UnaryOpNode:
    op: str
    operand: "ASTNode"

@dataclass
class AssignNode:
    name: str
    value_expr: "ASTNode"

@dataclass
class PrintNode:
    expr: "ASTNode"

@dataclass
class IfNode:
    condition: "ASTNode"
    body: List["ASTNode"]
    else_body: List["ASTNode"] = field(default_factory=list)

@dataclass
class WhileNode:
    condition: "ASTNode"
    body: List["ASTNode"]

ASTNode = Union[
    NumberNode, StringNode, BoolNode, VarNode,
    BinOpNode, UnaryOpNode,
    AssignNode, PrintNode, IfNode, WhileNode,
]


class ParseError(Exception):
    def __init__(self, message: str, line: int):
        self.line = line
        super().__init__(f"Parser Ghalati (line {line}): {message}")


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, "", -1)

    def _advance(self) -> Token:
        tok = self._current()
        self.pos += 1
        return tok

    def _expect(self, token_type: TokenType, value: Optional[str] = None) -> Token:
        tok = self._current()
        if tok.type != token_type:
            raise ParseError(f"'{value or token_type.name}' expected, lekin '{tok.value}' mila", tok.line)
        if value is not None and tok.value != value:
            raise ParseError(f"'{value}' expected, lekin '{tok.value}' mila", tok.line)
        return self._advance()

    def _skip_newlines(self) -> None:
        while self._current().type == TokenType.NEWLINE:
            self._advance()

    def _at_block_end(self) -> bool:
        tok = self._current()
        if tok.type == TokenType.EOF:
            return True
        if tok.type == TokenType.KEYWORD and tok.value in ("khatam", "warna"):
            return True
        return False

    def parse(self) -> List[ASTNode]:
        self._skip_newlines()
        stmts = self._parse_block(top_level=True)
        if self._current().type != TokenType.EOF:
            tok = self._current()
            raise ParseError(f"Unexpected token: '{tok.value}'", tok.line)
        return stmts

    def _parse_block(self, top_level: bool = False) -> List[ASTNode]:
        stmts: List[ASTNode] = []
        while True:
            self._skip_newlines()
            if self._current().type == TokenType.EOF:
                break
            if not top_level and self._at_block_end():
                break
            stmt = self._parse_statement()
            if stmt is not None:
                stmts.append(stmt)
        return stmts

    def _parse_statement(self) -> ASTNode:
        tok = self._current()
        if tok.type == TokenType.KEYWORD:
            if tok.value == "rakho":
                return self._parse_assign()
            elif tok.value == "dikhao":
                return self._parse_print()
            elif tok.value == "agar":
                return self._parse_if()
            elif tok.value == "jabtak":
                return self._parse_while()
            else:
                raise ParseError(f"Unexpected keyword: '{tok.value}'", tok.line)
        raise ParseError(f"Statement expected, lekin '{tok.value}' mila", tok.line)

    def _parse_assign(self) -> AssignNode:
        self._advance()
        name_tok = self._expect(TokenType.IDENTIFIER)
        self._expect(TokenType.ASSIGN, "=")
        expr = self._parse_expression()
        return AssignNode(name=name_tok.value, value_expr=expr)

    def _parse_print(self) -> PrintNode:
        self._advance()
        expr = self._parse_expression()
        return PrintNode(expr=expr)

    def _parse_if(self) -> IfNode:
        self._advance()
        condition = self._parse_expression()
        self._skip_newlines()
        body = self._parse_block()
        else_body: List[ASTNode] = []
        if self._current().type == TokenType.KEYWORD and self._current().value == "warna":
            self._advance()
            self._skip_newlines()
            else_body = self._parse_block()
        self._expect(TokenType.KEYWORD, "khatam")
        return IfNode(condition=condition, body=body, else_body=else_body)

    def _parse_while(self) -> WhileNode:
        self._advance()
        condition = self._parse_expression()
        self._skip_newlines()
        body = self._parse_block()
        self._expect(TokenType.KEYWORD, "khatam")
        return WhileNode(condition=condition, body=body)

    # ── Expression parsing with operator precedence ──

    def _parse_expression(self) -> ASTNode:
        return self._parse_or()

    def _parse_or(self) -> ASTNode:
        left = self._parse_and()
        while self._current().type == TokenType.KEYWORD and self._current().value == "ya":
            self._advance()
            right = self._parse_and()
            left = BinOpNode(left, "ya", right)
        return left

    def _parse_and(self) -> ASTNode:
        left = self._parse_comparison()
        while self._current().type == TokenType.KEYWORD and self._current().value == "aur":
            self._advance()
            right = self._parse_comparison()
            left = BinOpNode(left, "aur", right)
        return left

    def _parse_comparison(self) -> ASTNode:
        left = self._parse_addition()
        cmp_ops = {">", "<", ">=", "<=", "==", "!="}
        while self._current().type == TokenType.OPERATOR and self._current().value in cmp_ops:
            op = self._advance().value
            right = self._parse_addition()
            left = BinOpNode(left, op, right)
        return left

    def _parse_addition(self) -> ASTNode:
        left = self._parse_multiply()
        while self._current().type == TokenType.OPERATOR and self._current().value in ("+", "-"):
            op = self._advance().value
            right = self._parse_multiply()
            left = BinOpNode(left, op, right)
        return left

    def _parse_multiply(self) -> ASTNode:
        left = self._parse_unary()
        while self._current().type == TokenType.OPERATOR and self._current().value in ("*", "/"):
            op = self._advance().value
            right = self._parse_unary()
            left = BinOpNode(left, op, right)
        return left

    def _parse_unary(self) -> ASTNode:
        if self._current().type == TokenType.OPERATOR and self._current().value == "-":
            self._advance()
            operand = self._parse_primary()
            return UnaryOpNode("-", operand)
        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        tok = self._current()
        if tok.type == TokenType.NUMBER:
            self._advance()
            return NumberNode(int(tok.value))
        if tok.type == TokenType.FLOAT:
            self._advance()
            return NumberNode(float(tok.value))
        if tok.type == TokenType.STRING:
            self._advance()
            return StringNode(tok.value)
        if tok.type == TokenType.KEYWORD and tok.value == "sahi":
            self._advance()
            return BoolNode(True)
        if tok.type == TokenType.KEYWORD and tok.value == "ghalat":
            self._advance()
            return BoolNode(False)
        if tok.type == TokenType.IDENTIFIER:
            self._advance()
            return VarNode(tok.value)
        if tok.type == TokenType.LPAREN:
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN, ")")
            return expr
        raise ParseError(f"Expression expected, lekin '{tok.value}' mila", tok.line)
