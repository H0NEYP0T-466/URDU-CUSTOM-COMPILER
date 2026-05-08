"""
Urdu Custom Compiler - Parser (Recursive-Descent)
Converts tokens into an AST. No external libraries used.
Provides helpful error messages with "did you mean?" suggestions.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union
from .lexer import Token, TokenType


# -- AST Nodes --

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


# -- All valid keywords for "did you mean?" --
ALL_KEYWORDS = {
    "rakho": "variable assign karo (declare/assign)",
    "dikhao": "screen pe dikhao (print)",
    "agar": "agar condition sahi ho toh (if)",
    "warna": "nahi toh (else)",
    "jabtak": "jab tak condition sahi rahe (while loop)",
    "khatam": "block ka end (end block)",
    "sahi": "boolean true value",
    "ghalat": "boolean false value",
    "aur": "logical AND operator",
    "ya": "logical OR operator",
}


class ParseError(Exception):
    def __init__(self, message: str, line: int):
        self.line = line
        super().__init__(f"Parser Ghalati (line {line}): {message}")


def _levenshtein(a: str, b: str) -> int:
    """Simple Levenshtein edit distance."""
    if len(a) < len(b):
        return _levenshtein(b, a)
    if len(b) == 0:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            cost = 0 if ca == cb else 1
            curr.append(min(curr[j] + 1, prev[j + 1] + 1, prev[j] + cost))
        prev = curr
    return prev[len(b)]


def _suggest_keyword(word: str) -> Optional[str]:
    """Find the closest keyword if the word is a likely typo (distance <= 2)."""
    best_match = None
    best_dist = 3  # only suggest if distance <= 2
    for kw in ALL_KEYWORDS:
        dist = _levenshtein(word.lower(), kw.lower())
        if dist < best_dist:
            best_dist = dist
            best_match = kw
    return best_match


def _build_helpful_error(tok: Token) -> str:
    """Build a helpful, descriptive error message based on what was found."""
    word = tok.value

    # Check for common typos of keywords
    suggestion = _suggest_keyword(word)
    if suggestion and suggestion != word:
        meaning = ALL_KEYWORDS[suggestion]
        return (
            f"'{word}' koi valid keyword nahi hai. "
            f"Kya aap '{suggestion}' likhna chahte the? "
            f"({suggestion} = {meaning})"
        )

    # Give specific guidance based on what was found
    if tok.type == TokenType.IDENTIFIER:
        return (
            f"'{word}' ek variable naam hai, lekin yahan pe statement hona chahiye. "
            f"Har line 'rakho' (assign), 'dikhao' (print), 'agar' (if), ya 'jabtak' (while) se shuru honi chahiye."
        )

    if tok.type == TokenType.NUMBER or tok.type == TokenType.FLOAT:
        return (
            f"Yahan number '{word}' mila, lekin statement expected thi. "
            f"Number assign karne ke liye: rakho x = {word}"
        )

    if tok.type == TokenType.STRING:
        return (
            f"Yahan string mila, lekin statement expected thi. "
            f"String print karne ke liye: dikhao \"{word}\""
        )

    if tok.type == TokenType.OPERATOR:
        return (
            f"Operator '{word}' yahan nahi aa sakta. "
            f"Pehle ek statement likho jaise: rakho x = 5 {word} 3"
        )

    if tok.type == TokenType.EOF:
        return (
            f"Code achanak khatam ho gaya. "
            f"Kya aap 'khatam' likhna bhool gaye agar/jabtak block ke end mein?"
        )

    return (
        f"'{word}' yahan expected nahi tha. "
        f"Valid statements hain: rakho (assign), dikhao (print), agar (if), jabtak (while)"
    )


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
            # More helpful messages for common expectations
            if value == "khatam":
                raise ParseError(
                    f"'khatam' expected tha block band karne ke liye, lekin '{tok.value}' mila. "
                    f"Har 'agar' aur 'jabtak' ke baad 'khatam' likhna zaruri hai.",
                    tok.line
                )
            if value == "=":
                raise ParseError(
                    f"'=' expected tha assignment mein. Sahi tarika: rakho variable_naam = value",
                    tok.line
                )
            raise ParseError(
                f"'{value or token_type.name}' expected, lekin '{tok.value}' mila",
                tok.line
            )
        if value is not None and tok.value != value:
            if value == "khatam":
                suggestion = _suggest_keyword(tok.value)
                msg = f"'khatam' expected tha block band karne ke liye, lekin '{tok.value}' mila."
                if suggestion:
                    msg += f" Kya aap '{suggestion}' likhna chahte the?"
                raise ParseError(msg, tok.line)
            raise ParseError(
                f"'{value}' expected, lekin '{tok.value}' mila",
                tok.line
            )
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
            raise ParseError(
                f"Unexpected token: '{tok.value}'. "
                f"Kya extra 'khatam' ya koi aur cheez reh gayi hai?",
                tok.line
            )
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
                # Unknown keyword - give helpful suggestion
                suggestion = _suggest_keyword(tok.value)
                if suggestion:
                    meaning = ALL_KEYWORDS.get(suggestion, "")
                    raise ParseError(
                        f"'{tok.value}' ek valid statement keyword nahi hai. "
                        f"Kya aap '{suggestion}' likhna chahte the? ({meaning})",
                        tok.line
                    )
                raise ParseError(
                    f"'{tok.value}' yahan use nahi ho sakta. "
                    f"Statement 'rakho', 'dikhao', 'agar', ya 'jabtak' se shuru honi chahiye.",
                    tok.line
                )

        # Not a keyword - build helpful error
        raise ParseError(_build_helpful_error(tok), tok.line)

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

    # -- Expression parsing with operator precedence --

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

        # Helpful error for expression context
        if tok.type == TokenType.KEYWORD:
            raise ParseError(
                f"Yahan ek value (number, string, variable) expected thi, lekin keyword '{tok.value}' mila. "
                f"Keyword ko value ki jagah use nahi kar sakte.",
                tok.line
            )

        raise ParseError(
            f"Expression mein '{tok.value}' expected nahi tha. "
            f"Yahan number, string, variable, ya (expression) hona chahiye.",
            tok.line
        )
