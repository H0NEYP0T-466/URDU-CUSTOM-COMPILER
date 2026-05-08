"""
Urdu Custom Compiler — Three Address Code (TAC) Generator
Converts AST into a flat list of TAC instructions.
Each instruction is a simple string in one of these forms:
  ASSIGN:    x = 5
  BINOP:     t0 = x + y
  COPY:      x = t0
  PRINT:     print t0
  LABEL:     L0:
  IFFALSE:   iffalse t0 goto L1
  GOTO:      goto L2
  NOP:       nop
"""

from __future__ import annotations
from typing import List

from .parser import (
    ASTNode, NumberNode, StringNode, BoolNode, VarNode,
    BinOpNode, UnaryOpNode, AssignNode, PrintNode, IfNode, WhileNode,
)


class IRGenerator:
    """
    Converts AST nodes into Three Address Code instructions.

    Usage:
        tac = IRGenerator().generate(ast_nodes)
    """

    def __init__(self) -> None:
        self._temp_counter = 0    # for t0, t1, t2...
        self._label_counter = 0   # for L0, L1, L2...
        self._instructions: List[str] = []

    def generate(self, ast_nodes: List[ASTNode]) -> List[str]:
        """Generate TAC for the full program."""
        self._temp_counter = 0
        self._label_counter = 0
        self._instructions = []

        for node in ast_nodes:
            self._gen_stmt(node)

        return list(self._instructions)

    # ── Helpers ──

    def _new_temp(self) -> str:
        """Allocate a new temporary variable name."""
        name = f"t{self._temp_counter}"
        self._temp_counter += 1
        return name

    def _new_label(self) -> str:
        """Allocate a new label name."""
        name = f"L{self._label_counter}"
        self._label_counter += 1
        return name

    def _emit(self, instruction: str) -> None:
        """Append an instruction to the output."""
        self._instructions.append(instruction)

    # ── Statement generation ──

    def _gen_stmt(self, node: ASTNode) -> None:
        """Generate TAC for a single statement."""
        if isinstance(node, AssignNode):
            # Evaluate the right-hand side into a temp/value
            val = self._gen_expr(node.value_expr)
            self._emit(f"{node.name} = {val}")

        elif isinstance(node, PrintNode):
            val = self._gen_expr(node.expr)
            self._emit(f"print {val}")

        elif isinstance(node, IfNode):
            self._gen_if(node)

        elif isinstance(node, WhileNode):
            self._gen_while(node)

    def _gen_if(self, node: IfNode) -> None:
        """Generate TAC for if/else with labels and jumps."""
        cond = self._gen_expr(node.condition)

        if node.else_body:
            # Has else branch
            else_label = self._new_label()
            end_label = self._new_label()

            self._emit(f"iffalse {cond} goto {else_label}")

            # Then body
            for stmt in node.body:
                self._gen_stmt(stmt)
            self._emit(f"goto {end_label}")

            # Else body
            self._emit(f"{else_label}:")
            for stmt in node.else_body:
                self._gen_stmt(stmt)

            self._emit(f"{end_label}:")
            self._emit("nop")
        else:
            # No else
            end_label = self._new_label()
            self._emit(f"iffalse {cond} goto {end_label}")

            for stmt in node.body:
                self._gen_stmt(stmt)

            self._emit(f"{end_label}:")
            self._emit("nop")

    def _gen_while(self, node: WhileNode) -> None:
        """Generate TAC for while loop with labels and jumps."""
        start_label = self._new_label()
        end_label = self._new_label()

        self._emit(f"{start_label}:")
        cond = self._gen_expr(node.condition)
        self._emit(f"iffalse {cond} goto {end_label}")

        for stmt in node.body:
            self._gen_stmt(stmt)

        self._emit(f"goto {start_label}")
        self._emit(f"{end_label}:")
        self._emit("nop")

    # ── Expression generation (returns the name holding the result) ──

    def _gen_expr(self, node: ASTNode) -> str:
        """Generate TAC for an expression, return temp/literal holding result."""
        if isinstance(node, NumberNode):
            return str(node.value)

        if isinstance(node, StringNode):
            return f'"{node.value}"'

        if isinstance(node, BoolNode):
            return "sahi" if node.value else "ghalat"

        if isinstance(node, VarNode):
            return node.name

        if isinstance(node, UnaryOpNode):
            operand = self._gen_expr(node.operand)
            temp = self._new_temp()
            self._emit(f"{temp} = -{operand}")
            return temp

        if isinstance(node, BinOpNode):
            left = self._gen_expr(node.left)
            right = self._gen_expr(node.right)
            temp = self._new_temp()
            self._emit(f"{temp} = {left} {node.op} {right}")
            return temp

        # Fallback
        return "???"
