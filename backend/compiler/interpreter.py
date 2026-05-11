"""
Urdu Custom Compiler - Tree-Walk Interpreter
Evaluates AST nodes recursively, maintains scoped symbol table, collects output.
Supports block scoping: variables in agar/jabtak blocks are local.
Supports functions, arrays, user input, and type casting.
"""

from typing import Any, Dict, List, Optional, Union
from .parser import (
    ASTNode, NumberNode, StringNode, BoolNode, VarNode,
    BinOpNode, UnaryOpNode, AssignNode, PrintNode, IfNode, WhileNode,
    FuncDefNode, ReturnNode, FuncCallNode,
    ArrayLiteralNode, ArrayAccessNode, ArrayAssignNode,
    InputNode, TypeCastNode,
)


# Maximum iterations to prevent infinite loops
MAX_ITERATIONS = 10000
MAX_CALL_DEPTH = 100


class UrduRuntimeError(Exception):
    """Runtime error with descriptive Urdu message."""
    def __init__(self, message: str):
        super().__init__(f"Ghalati: {message}")


class ReturnSignal(Exception):
    """Flow control signal for function returns — NOT a real error."""
    def __init__(self, value: Any = None):
        self.value = value
        super().__init__("return")


class Environment:
    """A lexical scope that holds variable bindings."""

    def __init__(self, parent: Optional["Environment"] = None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent

    def get(self, name: str) -> Any:
        """Look up a variable, walking up the scope chain."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise UrduRuntimeError(f"'{name}' defined nahi hai")

    def set(self, name: str, value: Any) -> None:
        """Set a variable in this scope. If it exists in a parent scope, update there."""
        # Check if variable exists in current scope first
        if name in self.variables:
            self.variables[name] = value
            return
        # Check if it exists in any parent scope (for reassignment like rakho x = x - 1)
        if self.parent and self._exists_in_parent(name):
            self.parent.set(name, value)
            return
        # New variable: define in current scope
        self.variables[name] = value

    def _exists_in_parent(self, name: str) -> bool:
        """Check if variable exists anywhere in the parent chain."""
        if self.parent is None:
            return False
        if name in self.parent.variables:
            return True
        return self.parent._exists_in_parent(name)

    def has(self, name: str) -> bool:
        """Check if a variable exists in this scope or any parent."""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False


class Interpreter:
    """
    Tree-walk interpreter for the Urdu language AST.
    Supports block scoping for agar/jabtak blocks.
    Supports functions, arrays, user input, and type casting.

    Usage:
        interp = Interpreter()
        output = interp.execute(ast_nodes)
    """

    def __init__(self) -> None:
        self.env = Environment()    # global environment
        self.output: List[str] = []
        self.functions: Dict[str, FuncDefNode] = {}  # function name -> definition
        self.call_depth = 0         # recursion depth tracker
        self._inputs: List[str] = []  # pre-supplied input strings (for web API)
        self._input_index = 0        # current position in inputs list

    def execute(self, statements: List[ASTNode], inputs: Optional[List[str]] = None) -> List[str]:
        """Execute a list of AST statements and return collected output lines."""
        self.env = Environment()
        self.output = []
        self.functions = {}
        self.call_depth = 0
        self._inputs = inputs or []
        self._input_index = 0
        for stmt in statements:
            self._exec_node(stmt)
        return self.output

    # -- Statement execution --

    def _exec_node(self, node: ASTNode) -> None:
        """Execute a single statement node."""
        if isinstance(node, AssignNode):
            value = self._eval(node.value_expr)
            self.env.set(node.name, value)

        elif isinstance(node, PrintNode):
            value = self._eval(node.expr)
            self.output.append(self._to_string(value))

        elif isinstance(node, IfNode):
            condition = self._eval(node.condition)
            if self._is_truthy(condition):
                # Create a new scope for the if body
                self.env = Environment(parent=self.env)
                for stmt in node.body:
                    self._exec_node(stmt)
                self.env = self.env.parent  # pop scope
            else:
                if node.else_body:
                    # Create a new scope for the else body
                    self.env = Environment(parent=self.env)
                    for stmt in node.else_body:
                        self._exec_node(stmt)
                    self.env = self.env.parent  # pop scope

        elif isinstance(node, WhileNode):
            iterations = 0
            while self._is_truthy(self._eval(node.condition)):
                iterations += 1
                if iterations > MAX_ITERATIONS:
                    raise UrduRuntimeError(
                        f"Loop {MAX_ITERATIONS} iterations se zyada chal gaya -- infinite loop?"
                    )
                # Create a new scope for each iteration
                self.env = Environment(parent=self.env)
                for stmt in node.body:
                    self._exec_node(stmt)
                self.env = self.env.parent  # pop scope

        elif isinstance(node, FuncDefNode):
            # Store function definition
            self.functions[node.name] = node

        elif isinstance(node, ReturnNode):
            # Raise ReturnSignal to unwind the call stack
            value = self._eval(node.value) if node.value else None
            raise ReturnSignal(value)

        elif isinstance(node, FuncCallNode):
            # Function call as a statement (ignore return value)
            self._call_function(node.name, node.args)

        elif isinstance(node, ArrayAssignNode):
            arr = self.env.get(node.name)
            if not isinstance(arr, list):
                raise UrduRuntimeError(f"'{node.name}' ek array/list nahi hai")
            index = self._eval(node.index)
            if not isinstance(index, int):
                raise UrduRuntimeError(f"Array index sirf integer hona chahiye")
            if index < 0 or index >= len(arr):
                raise UrduRuntimeError(
                    f"Array index {index} out of range hai -- array ki length {len(arr)} hai"
                )
            value = self._eval(node.value)
            arr[index] = value

        else:
            raise UrduRuntimeError(f"Unknown statement type: {type(node).__name__}")

    # -- Function calling --

    def _call_function(self, name: str, arg_nodes: List[ASTNode]) -> Any:
        """Call a function by name with given argument expressions."""
        if name not in self.functions:
            raise UrduRuntimeError(f"Function '{name}' defined nahi hai")

        func = self.functions[name]

        # Evaluate arguments in current environment
        arg_values = [self._eval(arg) for arg in arg_nodes]

        # Validate argument count
        if len(arg_values) != len(func.params):
            raise UrduRuntimeError(
                f"Function '{name}' ko {len(func.params)} arguments chahiye, "
                f"lekin {len(arg_values)} diye gaye"
            )

        # Check recursion depth
        self.call_depth += 1
        if self.call_depth > MAX_CALL_DEPTH:
            raise UrduRuntimeError(
                f"Function call {MAX_CALL_DEPTH} depth se zyada ho gaya -- infinite recursion?"
            )

        # Create new environment for function (linked to global, not caller)
        func_env = Environment(parent=self.env)
        for param_name, arg_val in zip(func.params, arg_values):
            func_env.variables[param_name] = arg_val

        # Save and switch environment
        saved_env = self.env
        self.env = func_env

        return_value = None
        try:
            for stmt in func.body:
                self._exec_node(stmt)
        except ReturnSignal as ret:
            return_value = ret.value
        finally:
            # Restore environment and call depth
            self.env = saved_env
            self.call_depth -= 1

        return return_value

    # -- Expression evaluation --

    def _eval(self, node: ASTNode) -> Any:
        """Evaluate an expression node and return its value."""
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, BoolNode):
            return node.value

        if isinstance(node, VarNode):
            return self.env.get(node.name)

        if isinstance(node, UnaryOpNode):
            operand = self._eval(node.operand)
            if node.op == "-":
                if not isinstance(operand, (int, float)):
                    raise UrduRuntimeError(f"Minus sirf numbers ke liye hai, '{type(operand).__name__}' nahi")
                return -operand

        if isinstance(node, BinOpNode):
            return self._eval_binop(node)

        if isinstance(node, FuncCallNode):
            return self._call_function(node.name, node.args)

        if isinstance(node, ArrayLiteralNode):
            return [self._eval(elem) for elem in node.elements]

        if isinstance(node, ArrayAccessNode):
            arr = self._eval(node.array)
            if not isinstance(arr, list):
                raise UrduRuntimeError(f"Index access sirf arrays/lists pe ho sakta hai")
            index = self._eval(node.index)
            if not isinstance(index, int):
                raise UrduRuntimeError(f"Array index sirf integer hona chahiye")
            if index < 0 or index >= len(arr):
                raise UrduRuntimeError(
                    f"Array index {index} out of range hai -- array ki length {len(arr)} hai"
                )
            return arr[index]

        if isinstance(node, InputNode):
            return self._handle_input(node)

        if isinstance(node, TypeCastNode):
            return self._handle_typecast(node)

        raise UrduRuntimeError(f"Unknown expression type: {type(node).__name__}")

    def _handle_input(self, node: InputNode) -> str:
        """Handle input() — use pre-supplied inputs for web, real input() for terminal."""
        prompt = ""
        if node.prompt:
            prompt = self._to_string(self._eval(node.prompt))

        if self._input_index < len(self._inputs):
            # Use pre-supplied input (web API mode)
            value = self._inputs[self._input_index]
            self._input_index += 1
            if prompt:
                self.output.append(f"{prompt}{value}")
            return value
        else:
            # No more pre-supplied inputs — return empty string
            if prompt:
                self.output.append(prompt)
            return ""

    def _handle_typecast(self, node: TypeCastNode) -> Any:
        """Handle int() and str() type casting."""
        value = self._eval(node.expr)
        if node.target_type == "int":
            try:
                if isinstance(value, float):
                    return int(value)
                if isinstance(value, bool):
                    return 1 if value else 0
                return int(value)
            except (ValueError, TypeError):
                raise UrduRuntimeError(
                    f"'{self._to_string(value)}' ko int mein convert nahi kar sakte"
                )
        if node.target_type == "str":
            return self._to_string(value)
        raise UrduRuntimeError(f"Unknown type cast: '{node.target_type}'")

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

    # -- Helpers --

    @staticmethod
    def _is_truthy(value: Any) -> bool:
        """Determine truthiness of a value."""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, list):
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
        if isinstance(value, list):
            items = ", ".join(Interpreter._to_string(v) for v in value)
            return f"[{items}]"
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
        if isinstance(value, list):
            return "array"
        return type(value).__name__
