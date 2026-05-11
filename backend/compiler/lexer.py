"""
Urdu Custom Compiler — Lexer (Tokenizer)
=========================================
Hand-written lexer that converts raw source code into a list of Token objects.
Supports Roman-Urdu keywords, identifiers, numbers, strings, and operators.
No external compiler libraries (PLY, ANTLR, etc.) are used.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List


# ──────────────────────────────────────────────
# Token Types
# ──────────────────────────────────────────────

class TokenType(Enum):
    """All token categories recognised by the Urdu language."""
    KEYWORD     = auto()   # rakho, dikhao, agar, warna, jabtak, khatam, sahi, ghalat, aur, ya, functionbnao, wapisbejo
    IDENTIFIER  = auto()   # variable names
    NUMBER      = auto()   # integer literals
    FLOAT       = auto()   # floating-point literals
    STRING      = auto()   # string literals (double-quoted)
    OPERATOR    = auto()   # +  -  *  /  >  <  >=  <=  ==  !=
    ASSIGN      = auto()   # =
    LPAREN      = auto()   # (
    RPAREN      = auto()   # )
    COMMA       = auto()   # ,
    LBRACKET    = auto()   # [
    RBRACKET    = auto()   # ]
    NEWLINE     = auto()   # logical line separator
    EOF         = auto()   # end of file


# ──────────────────────────────────────────────
# Token data class
# ──────────────────────────────────────────────

@dataclass
class Token:
    """A single token produced by the lexer."""
    type: TokenType
    value: str
    line: int              # 1-based line number

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, line={self.line})"


# ──────────────────────────────────────────────
# Custom error for lexing failures
# ──────────────────────────────────────────────

class LexError(Exception):
    """Raised when the lexer encounters an invalid character or malformed token."""
    def __init__(self, message: str, line: int):
        self.line = line
        super().__init__(f"Lexer Ghalati (line {line}): {message}")


# ──────────────────────────────────────────────
# Reserved keywords set
# ──────────────────────────────────────────────

KEYWORDS = {
    "rakho", "dikhao", "agar", "warna",
    "jabtak", "khatam", "sahi", "ghalat",
    "aur", "ya",
    "functionbnao", "wapisbejo",
}

# Multi-character operators (checked first so '>' is not consumed before '>=')
MULTI_CHAR_OPS = {">=", "<=", "==", "!="}

# Single-character operators
SINGLE_CHAR_OPS = {"+", "-", "*", "/", ">", "<"}


# ──────────────────────────────────────────────
# Lexer class
# ──────────────────────────────────────────────

class Lexer:
    """
    Converts raw source text into a flat list of Token objects.

    Usage:
        tokens = Lexer(source_code).tokenize()
    """

    def __init__(self, source: str):
        self.source = source
        self.pos = 0                   # current character index
        self.line = 1                  # current line number (1-based)
        self.tokens: List[Token] = []

    # ── helpers ──────────────────────────────

    def _current(self) -> str:
        """Return the character at the current position, or '' if at end."""
        if self.pos < len(self.source):
            return self.source[self.pos]
        return ""

    def _peek(self, offset: int = 1) -> str:
        """Look ahead by *offset* characters without advancing."""
        idx = self.pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return ""

    def _advance(self) -> str:
        """Consume the current character and return it."""
        ch = self._current()
        if ch == "\n":
            self.line += 1
        self.pos += 1
        return ch

    def _skip_whitespace(self) -> None:
        """Skip spaces and tabs (NOT newlines — those are tokens)."""
        while self.pos < len(self.source) and self._current() in (" ", "\t", "\r"):
            self._advance()

    def _skip_comment(self) -> None:
        """Skip single-line comments starting with '#'."""
        while self.pos < len(self.source) and self._current() != "\n":
            self._advance()

    # ── sub-scanners ─────────────────────────

    def _read_string(self) -> Token:
        """Read a double-quoted string literal."""
        start_line = self.line
        self._advance()  # consume opening "
        value = ""
        while self.pos < len(self.source) and self._current() != '"':
            if self._current() == "\n":
                raise LexError("String band nahi hui (missing closing quote)", start_line)
            value += self._advance()
        if self.pos >= len(self.source):
            raise LexError("String band nahi hui (missing closing quote)", start_line)
        self._advance()  # consume closing "
        return Token(TokenType.STRING, value, start_line)

    def _read_number(self) -> Token:
        """Read an integer or float literal."""
        start_line = self.line
        num_str = ""
        has_dot = False
        while self.pos < len(self.source) and (self._current().isdigit() or self._current() == "."):
            if self._current() == ".":
                if has_dot:
                    raise LexError(f"Number mein zyada dots: '{num_str}.'", start_line)
                has_dot = True
            num_str += self._advance()
        if has_dot:
            return Token(TokenType.FLOAT, num_str, start_line)
        return Token(TokenType.NUMBER, num_str, start_line)

    def _read_word(self) -> Token:
        """Read a keyword or identifier (alphanumeric + underscores)."""
        start_line = self.line
        word = ""
        while self.pos < len(self.source) and (self._current().isalnum() or self._current() == "_"):
            word += self._advance()
        if word in KEYWORDS:
            return Token(TokenType.KEYWORD, word, start_line)
        return Token(TokenType.IDENTIFIER, word, start_line)

    # ── main tokenize loop ───────────────────

    def tokenize(self) -> List[Token]:
        """
        Scan the entire source and return a list of tokens
        terminated by an EOF token.
        """
        while self.pos < len(self.source):
            ch = self._current()

            # ── skip whitespace (spaces / tabs) ──
            if ch in (" ", "\t", "\r"):
                self._skip_whitespace()
                continue

            # ── newlines → NEWLINE tokens ──
            if ch == "\n":
                # Avoid consecutive NEWLINE tokens
                if not self.tokens or self.tokens[-1].type != TokenType.NEWLINE:
                    self.tokens.append(Token(TokenType.NEWLINE, "\\n", self.line))
                self._advance()
                continue

            # ── comments ──
            if ch == "#":
                self._skip_comment()
                continue

            # ── string literals ──
            if ch == '"':
                self.tokens.append(self._read_string())
                continue

            # ── numbers ──
            if ch.isdigit():
                self.tokens.append(self._read_number())
                continue

            # ── words (keywords / identifiers) ──
            if ch.isalpha() or ch == "_":
                self.tokens.append(self._read_word())
                continue

            # ── multi-character operators (>=, <=, ==, !=) ──
            two_char = ch + self._peek()
            if two_char in MULTI_CHAR_OPS:
                line = self.line
                self._advance()
                self._advance()
                self.tokens.append(Token(TokenType.OPERATOR, two_char, line))
                continue

            # ── single-character operators ──
            if ch in SINGLE_CHAR_OPS:
                line = self.line
                self._advance()
                self.tokens.append(Token(TokenType.OPERATOR, ch, line))
                continue

            # ── assignment ──
            if ch == "=":
                self.tokens.append(Token(TokenType.ASSIGN, "=", self.line))
                self._advance()
                continue

            # ── parentheses ──
            if ch == "(":
                self.tokens.append(Token(TokenType.LPAREN, "(", self.line))
                self._advance()
                continue
            if ch == ")":
                self.tokens.append(Token(TokenType.RPAREN, ")", self.line))
                self._advance()
                continue

            # ── comma ──
            if ch == ",":
                self.tokens.append(Token(TokenType.COMMA, ",", self.line))
                self._advance()
                continue

            # ── brackets ──
            if ch == "[":
                self.tokens.append(Token(TokenType.LBRACKET, "[", self.line))
                self._advance()
                continue
            if ch == "]":
                self.tokens.append(Token(TokenType.RBRACKET, "]", self.line))
                self._advance()
                continue

            # ── unknown character ──
            raise LexError(f"Anjaan character: '{ch}'", self.line)

        # Append EOF
        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens
