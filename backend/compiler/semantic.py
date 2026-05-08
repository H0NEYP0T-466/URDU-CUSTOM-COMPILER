"""
Urdu Custom Compiler -- Semantic Analyzer
Walks the AST before interpretation to catch errors statically:
  1. Undefined variable references
  2. Re-declaration warnings
  3. Type mismatch in operations
  4. Static division by zero
  5. Block scoping (agar/jabtak create child scopes)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


from .parser import (
    ASTNode, NumberNode, StringNode, BoolNode, VarNode,
    BinOpNode, UnaryOpNode, AssignNode, PrintNode, IfNode, WhileNode,
)


# -- Type constants --
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
class SymbolEntry:
    """A single entry in the symbol table."""
    name: str
    var_type: str
    scope: str           # e.g. "global", "agar:1", "jabtak:2"
    scope_depth: int     # 0 = global, 1 = first nesting, etc.


@dataclass
class SemanticResult:
    """Result of semantic analysis."""
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    symbol_table: Dict[str, str] = field(default_factory=dict)
    scoped_symbols: List[SymbolEntry] = field(default_factory=list)


class SemanticError(Exception):
    """Raised to signal a fatal semantic error."""
    def __init__(self, message: str):
        super().__init__(f"Semantic Ghalati: {message}")


class Scope:
    """A single lexical scope that holds variable->type mappings."""

    def __init__(self, name: str, depth: int, parent: Optional["Scope"] = None):
        self.name = name
        self.depth = depth
        self.parent = parent
        self.variables: Dict[str, str] = {}

    def define(self, var_name: str, var_type: str) -> None:
        """Define a variable in this scope."""
        self.variables[var_name] = var_type

    def lookup(self, var_name: str) -> Optional[str]:
        """Look up a variable, walking up the scope chain."""
        if var_name in self.variables:
            return self.variables[var_name]
        if self.parent:
            return self.parent.lookup(var_name)
        return None

    def is_defined_locally(self, var_name: str) -> bool:
        """Check if a variable is defined in THIS scope (not parent)."""
        return var_name in self.variables

    def is_defined_anywhere(self, var_name: str) -> bool:
        """Check if a variable is defined anywhere in the scope chain."""
        return self.lookup(var_name) is not None


class SemanticAnalyzer:
    """
    Walks the AST and performs static checks before interpretation.
    Uses a scope stack for block scoping.

    Usage:
        result = SemanticAnalyzer().analyze(ast_nodes)
        if result.errors: ...handle errors...
    """

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.all_symbols: List[SymbolEntry] = []
        self._scope_counter = 0

        # Initialize global scope
        self.global_scope = Scope("global", 0)
        self.current_scope = self.global_scope

    def analyze(self, ast_nodes: List[ASTNode]) -> SemanticResult:
        """Analyze all top-level statements and return result."""
        self.errors = []
        self.warnings = []
        self.all_symbols = []
        self._scope_counter = 0
        self.global_scope = Scope("global", 0)
        self.current_scope = self.global_scope

        for node in ast_nodes:
            self._check_node(node)

        # Build flat symbol_table (for backward compat) from all scopes
        flat_table: Dict[str, str] = {}
        for entry in self.all_symbols:
            key = entry.name if entry.scope == "global" else f"{entry.name} ({entry.scope})"
            flat_table[key] = entry.var_type

        return SemanticResult(
            errors=list(self.errors),
            warnings=list(self.warnings),
            symbol_table=flat_table,
            scoped_symbols=list(self.all_symbols),
        )

    # -- Scope management --

    def _push_scope(self, scope_name: str) -> None:
        """Create and enter a new child scope."""
        self._scope_counter += 1
        new_scope = Scope(
            name=f"{scope_name}:{self._scope_counter}",
            depth=self.current_scope.depth + 1,
            parent=self.current_scope,
        )
        self.current_scope = new_scope

    def _pop_scope(self) -> None:
        """Exit the current scope and return to parent."""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent

    # -- Statement checking --

    def _check_node(self, node: ASTNode) -> None:
        """Check a single statement node for semantic errors."""
        if isinstance(node, AssignNode):
            self._check_assign(node)
        elif isinstance(node, PrintNode):
            self._check_expr(node.expr)
        elif isinstance(node, IfNode):
            self._check_expr(node.condition)
            # agar body gets its own scope
            self._push_scope("agar")
            for stmt in node.body:
                self._check_node(stmt)
            self._pop_scope()
            # warna body gets its own scope
            if node.else_body:
                self._push_scope("warna")
                for stmt in node.else_body:
                    self._check_node(stmt)
                self._pop_scope()
        elif isinstance(node, WhileNode):
            self._check_expr(node.condition)
            # jabtak body gets its own scope
            self._push_scope("jabtak")
            for stmt in node.body:
                self._check_node(stmt)
            self._pop_scope()

    def _check_assign(self, node: AssignNode) -> None:
        """Check assignment: warn on re-declaration in same scope, infer type."""
        # Re-declaration warning (only within same scope)
        if self.current_scope.is_defined_locally(node.name):
            self.warnings.append(
                f"Variable '{node.name}' is scope mein pehle se defined hai -- dubara assign ho rahi hai"
            )

        # Check the value expression
        expr_type = self._check_expr(node.value_expr)
        resolved_type = expr_type or TYPE_UNKNOWN

        # Define in current scope
        self.current_scope.define(node.name, resolved_type)

        # Track for symbol table output
        self.all_symbols.append(SymbolEntry(
            name=node.name,
            var_type=resolved_type,
            scope=self.current_scope.name,
            scope_depth=self.current_scope.depth,
        ))

    # -- Expression checking (returns inferred type) --

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
        """Check that a variable is defined in current or parent scope."""
        result = self.current_scope.lookup(node.name)
        if result is None:
            self.errors.append(
                f"Variable '{node.name}' defined nahi hai -- pehle 'rakho' se assign karo"
            )
            return TYPE_UNKNOWN
        return result

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

        # Logical operators -- any type is fine
        if op in ("aur", "ya"):
            return TYPE_BOOL

        # Comparison operators -- need numeric operands (except == and !=)
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

        # Arithmetic operators -- need numeric operands
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
