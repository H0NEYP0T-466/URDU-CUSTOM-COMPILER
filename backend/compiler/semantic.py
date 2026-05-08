"""
Urdu Custom Compiler — Semantic Analyzer
Walks the AST before interpretation to catch errors statically:
  1. Undefined variable references
  2. Re-declaration warnings
  3. Type mismatch in operations
  4. Static division by zero
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .parser import (
    ASTNode, NumberNode, StringNode, BoolNode, VarNode,
    BinOpNode, UnaryOpNode, AssignNode, PrintNode, IfNode, WhileNode,
)


# ── Type constants ──
TYPE_INT = "int"
TYPE_FLOAT = "float"
TYPE_STRING = "string"
TYPE_BOOL = "bool"
TYPE_NUMBER = "number"   # used when int/float are interchangeable
TYPE_UNKNOWN = "unknown"

# Operators that require numeric operands
ARITHMETIC_OPS = {"+", "-", "*", "/"}
COMPARISON_OPS = {">", "<", ">=", "<="}


@dataclass
class SemanticResult:
    """Result of semantic analysis."""
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    symbol_table: Dict[str, str] = field(default_factory=dict)


class SemanticError(Exception):
    """Raised to signal a fatal semantic error."""
    def __init__(self, message: str):
        super().__init__(f"Semantic Ghalati: {message}")


class SemanticAnalyzer:
    """
    Walks the AST and performs static checks before interpretation.

    Usage:
        result = SemanticAnalyzer().analyze(ast_nodes)
        if result.errors: ...handle errors...
    """

    def __init__(self) -> None:
        self.symbol_table: Dict[str, str] = {}   # var_name → type_string
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def analyze(self, ast_nodes: List[ASTNode]) -> SemanticResult:
        """Analyze all top-level statements and return result."""
        self.symbol_table = {}
        self.errors = []
        self.warnings = []

        for node in ast_nodes:
            self._check_node(node)

        return SemanticResult(
            errors=list(self.errors),
            warnings=list(self.warnings),
            symbol_table=dict(self.symbol_table),
        )

    # ── Statement checking ──

    def _check_node(self, node: ASTNode) -> None:
        """Check a single statement node for semantic errors."""
        if isinstance(node, AssignNode):
            self._check_assign(node)
        elif isinstance(node, PrintNode):
            self._check_expr(node.expr)
        elif isinstance(node, IfNode):
            self._check_expr(node.condition)
            for stmt in node.body:
                self._check_node(stmt)
            for stmt in node.else_body:
                self._check_node(stmt)
        elif isinstance(node, WhileNode):
            self._check_expr(node.condition)
            for stmt in node.body:
                self._check_node(stmt)

    def _check_assign(self, node: AssignNode) -> None:
        """Check assignment: warn on re-declaration, infer type."""
        # Re-declaration warning
        if node.name in self.symbol_table:
            self.warnings.append(
                f"Variable '{node.name}' pehle se defined hai -- dubara assign ho rahi hai"
            )

        # Check the value expression
        expr_type = self._check_expr(node.value_expr)

        # Store inferred type
        self.symbol_table[node.name] = expr_type or TYPE_UNKNOWN

    # ── Expression checking (returns inferred type) ──

    def _check_expr(self, node: ASTNode) -> Optional[str]:
        """Check an expression node and return its inferred type string."""
        if isinstance(node, NumberNode):
            if isinstance(node.value, float):
                return TYPE_FLOAT
            return TYPE_INT

        if isinstance(node, StringNode):
            return TYPE_STRING

        if isinstance(node, BoolNode):
            return TYPE_BOOL

        if isinstance(node, VarNode):
            return self._check_var(node)

        if isinstance(node, UnaryOpNode):
            operand_type = self._check_expr(node.operand)
            if operand_type == TYPE_STRING:
                self.errors.append(
                    f"Minus (-) operator string pe nahi lag sakta"
                )
            return operand_type

        if isinstance(node, BinOpNode):
            return self._check_binop(node)

        return TYPE_UNKNOWN

    def _check_var(self, node: VarNode) -> Optional[str]:
        """Check that a variable is defined, return its type."""
        if node.name not in self.symbol_table:
            self.errors.append(
                f"Variable '{node.name}' defined nahi hai -- pehle 'rakho' se assign karo"
            )
            return TYPE_UNKNOWN
        return self.symbol_table[node.name]

    def _check_binop(self, node: BinOpNode) -> Optional[str]:
        """Check a binary operation for type compatibility."""
        left_type = self._check_expr(node.left)
        right_type = self._check_expr(node.right)
        op = node.op

        # Static division by zero check
        if op == "/" and isinstance(node.right, NumberNode) and node.right.value == 0:
            self.errors.append(
                f"Zero (0) se divide nahi kar sakte -- division by zero"
            )

        # Logical operators — any type is fine
        if op in ("aur", "ya"):
            return TYPE_BOOL

        # Comparison operators — need numeric operands (except == and !=)
        if op in COMPARISON_OPS:
            if left_type == TYPE_STRING or right_type == TYPE_STRING:
                self.errors.append(
                    f"Comparison '{op}' strings ke saath nahi ho sakti"
                )
            return TYPE_BOOL

        if op in ("==", "!="):
            return TYPE_BOOL

        # String concatenation with +
        if op == "+":
            if left_type == TYPE_STRING and right_type == TYPE_STRING:
                return TYPE_STRING
            if left_type == TYPE_STRING or right_type == TYPE_STRING:
                # One is string, other is not
                if left_type != TYPE_UNKNOWN and right_type != TYPE_UNKNOWN:
                    self.errors.append(
                        f"'+' operator: STRING aur {right_type if left_type == TYPE_STRING else left_type} ko jor nahi sakte"
                    )
                return TYPE_UNKNOWN

        # Arithmetic operators — need numeric operands
        if op in ("-", "*", "/"):
            if left_type == TYPE_STRING:
                self.errors.append(
                    f"'{op}' operator STRING pe nahi chal sakta"
                )
            if right_type == TYPE_STRING:
                self.errors.append(
                    f"'{op}' operator STRING pe nahi chal sakta"
                )

        # Infer result type for arithmetic
        if left_type == TYPE_FLOAT or right_type == TYPE_FLOAT:
            return TYPE_FLOAT
        if op == "/":
            return TYPE_FLOAT  # division always returns float
        if left_type == TYPE_INT and right_type == TYPE_INT:
            return TYPE_INT

        return TYPE_NUMBER
