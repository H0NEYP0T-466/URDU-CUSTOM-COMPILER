"""
Urdu Custom Compiler - Tree-Walk Interpreter
Evaluates AST nodes recursively, maintains symbol table, collects output.
"""

from typing import Any, Dict, List, Union
from .parser import (
    ASTNode, NumberNode, StringNode, BoolNode, VarNode,
    BinOpNode, UnaryOpNode, AssignNode, PrintNode, IfNode, WhileNode,
)


# Maximum iterations to prevent infinite loops
MAX_ITERATIONS = 10000


class UrduRuntimeError(Exception):
    """Runtime error with descriptive Urdu message."""
    def __init__(self, message: str):
        super().__init__(f"Ghalati: {message}")


class Interpreter:
    """
    Tree-walk interpreter for the Urdu language AST.

    Usage:
        interp = Interpreter()
        output = interp.execute(ast_nodes)
    """

    def __init__(self) -> None:
        self.variables: Dict[str, Any] = {}
        self.output: List[str] = []

    def execute(self, statements: List[ASTNode]) -> List[str]:
        """Execute a list of AST statements and return collected output lines."""
        self.variables = {}
        self.output = []
        for stmt in statements:
            self._exec_node(stmt)
        return self.output

    # ── Statement execution ──

    def _exec_node(self, node: ASTNode) -> None:
        """Execute a single statement node."""
        if isinstance(node, AssignNode):
            value = self._eval(node.value_expr)
            self.variables[node.name] = value

        elif isinstance(node, PrintNode):
            value = self._eval(node.expr)
            self.output.append(self._to_string(value))

        elif isinstance(node, IfNode):
            condition = self._eval(node.condition)
            if self._is_truthy(condition):
                for stmt in node.body:
                    self._exec_node(stmt)
            else:
                for stmt in node.else_body:
                    self._exec_node(stmt)

        elif isinstance(node, WhileNode):
            iterations = 0
            while self._is_truthy(self._eval(node.condition)):
                iterations += 1
                if iterations > MAX_ITERATIONS:
                    raise UrduRuntimeError(
                        f"Loop {MAX_ITERATIONS} iterations se zyada chal gaya — infinite loop?"
                    )
                for stmt in node.body:
                    self._exec_node(stmt)

        else:
            raise UrduRuntimeError(f"Unknown statement type: {type(node).__name__}")

    # ── Expression evaluation ──

    def _eval(self, node: ASTNode) -> Any:
        """Evaluate an expression node and return its value."""
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, BoolNode):
            return node.value

        if isinstance(node, VarNode):
            if node.name not in self.variables:
                raise UrduRuntimeError(f"'{node.name}' defined nahi hai")
            return self.variables[node.name]

        if isinstance(node, UnaryOpNode):
            operand = self._eval(node.operand)
            if node.op == "-":
                if not isinstance(operand, (int, float)):
                    raise UrduRuntimeError(f"Minus sirf numbers ke liye hai, '{type(operand).__name__}' nahi")
                return -operand

        if isinstance(node, BinOpNode):
            return self._eval_binop(node)

        raise UrduRuntimeError(f"Unknown expression type: {type(node).__name__}")

    def _eval_binop(self, node: BinOpNode) -> Any:
        """Evaluate a binary operation."""
        left = self._eval(node.left)
        right = self._eval(node.right)
        op = node.op

        # Logical operators
        if op == "aur":
            return self._is_truthy(left) and self._is_truthy(right)
        if op == "ya":
            return self._is_truthy(left) or self._is_truthy(right)

        # Comparison operators
        if op == "==":
            return left == right
        if op == "!=":
            return left != right

        if op in (">", "<", ">=", "<="):
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise UrduRuntimeError(
                    f"Comparison sirf numbers mein hoti hai, '{self._type_name(left)}' aur '{self._type_name(right)}' nahi"
                )
            if op == ">":
                return left > right
            if op == "<":
                return left < right
            if op == ">=":
                return left >= right
            if op == "<=":
                return left <= right

        # Arithmetic: addition also handles string concatenation
        if op == "+":
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            raise UrduRuntimeError(
                f"'+' ke liye dono taraf same type honi chahiye (number ya string)"
            )

        if op in ("-", "*", "/"):
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise UrduRuntimeError(
                    f"'{op}' sirf numbers ke liye hai"
                )
            if op == "-":
                return left - right
            if op == "*":
                return left * right
            if op == "/":
                if right == 0:
                    raise UrduRuntimeError("Zero se divide nahi kar sakte!")
                return left / right

        raise UrduRuntimeError(f"Unknown operator: '{op}'")

    # ── Helpers ──

    @staticmethod
    def _is_truthy(value: Any) -> bool:
        """Determine truthiness of a value."""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        return False

    @staticmethod
    def _to_string(value: Any) -> str:
        """Convert a value to its display string."""
        if isinstance(value, bool):
            return "sahi" if value else "ghalat"
        if isinstance(value, float):
            if value == int(value):
                return str(int(value))
            return str(value)
        return str(value)

    @staticmethod
    def _type_name(value: Any) -> str:
        """Return a user-friendly type name."""
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, int):
            return "number"
        if isinstance(value, float):
            return "number"
        if isinstance(value, str):
            return "string"
        return type(value).__name__
