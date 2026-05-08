"""
Urdu Custom Compiler — TAC Optimizer
Applies three optimizations to the Three Address Code:
  1. Constant Folding    — evaluate constant expressions at compile time
  2. Constant Propagation — replace variable uses with known literal values
  3. Dead Code Elimination — remove unused temp assignments
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class OptimizeResult:
    """Result of the optimization pass."""
    original: List[str]       # TAC before optimization
    optimized: List[str]      # TAC after optimization
    changes: List[str]        # human-readable log of changes


class Optimizer:
    """
    Applies optimization passes to a list of TAC instruction strings.

    Usage:
        result = Optimizer().optimize(tac_instructions)
    """

    def optimize(self, tac: List[str]) -> OptimizeResult:
        """Run all optimization passes and return result."""
        original = list(tac)
        changes: List[str] = []

        # Pass 1: Constant Propagation
        tac, prop_changes = self._constant_propagation(tac)
        changes.extend(prop_changes)

        # Pass 2: Constant Folding
        tac, fold_changes = self._constant_folding(tac)
        changes.extend(fold_changes)

        # Pass 3: Run folding again after propagation may have revealed new constants
        tac, fold_changes2 = self._constant_folding(tac)
        changes.extend(fold_changes2)

        # Pass 4: Dead Code Elimination
        tac, dce_changes = self._dead_code_elimination(tac)
        changes.extend(dce_changes)

        if not changes:
            changes.append("No optimizations applicable")

        return OptimizeResult(
            original=original,
            optimized=tac,
            changes=changes,
        )

    # ═══════════════════════════════════════════
    # Pass 1: Constant Folding
    # ═══════════════════════════════════════════

    def _constant_folding(self, tac: List[str]) -> tuple[List[str], List[str]]:
        """Evaluate constant arithmetic expressions at compile time."""
        result: List[str] = []
        changes: List[str] = []

        # Pattern: t0 = <num> <op> <num>
        pattern = re.compile(
            r'^(\w+)\s*=\s*(-?\d+(?:\.\d+)?)\s*([+\-*/><]|>=|<=|==|!=)\s*(-?\d+(?:\.\d+)?)$'
        )

        for line in tac:
            match = pattern.match(line.strip())
            if match:
                dest = match.group(1)
                left_str = match.group(2)
                op = match.group(3)
                right_str = match.group(4)

                left_val = float(left_str) if '.' in left_str else int(left_str)
                right_val = float(right_str) if '.' in right_str else int(right_str)

                folded = self._try_fold(left_val, op, right_val)
                if folded is not None:
                    folded_str = self._format_value(folded)
                    new_line = f"{dest} = {folded_str}"
                    result.append(new_line)
                    changes.append(f"Constant folding: {line.strip()} --> {new_line}")
                    continue

            result.append(line)

        return result, changes

    @staticmethod
    def _try_fold(left: float | int, op: str, right: float | int) -> Optional[float | int | bool]:
        """Attempt to evaluate a binary operation on constants."""
        try:
            if op == "+":
                return left + right
            elif op == "-":
                return left - right
            elif op == "*":
                return left * right
            elif op == "/":
                if right == 0:
                    return None  # don't fold division by zero
                return left / right
            elif op == ">":
                return left > right
            elif op == "<":
                return left < right
            elif op == ">=":
                return left >= right
            elif op == "<=":
                return left <= right
            elif op == "==":
                return left == right
            elif op == "!=":
                return left != right
        except Exception:
            return None
        return None

    @staticmethod
    def _format_value(value: float | int | bool) -> str:
        """Format a folded constant for output."""
        if isinstance(value, bool):
            return "sahi" if value else "ghalat"
        if isinstance(value, float):
            if value == int(value):
                return str(int(value))
            return str(value)
        return str(value)

    # ═══════════════════════════════════════════
    # Pass 2: Constant Propagation (simple)
    # ═══════════════════════════════════════════

    def _constant_propagation(self, tac: List[str]) -> tuple[List[str], List[str]]:
        """Replace uses of variables with their known constant values."""
        result: List[str] = []
        changes: List[str] = []

        # Track which variables have a known constant value
        constants: Dict[str, str] = {}

        # First pass: find variables assigned a single literal
        assign_pattern = re.compile(r'^(\w+)\s*=\s*(-?\d+(?:\.\d+)?|"[^"]*"|sahi|ghalat)$')
        # Track how many times each var is assigned (skip if reassigned)
        assign_counts: Dict[str, int] = {}

        for line in tac:
            m = re.match(r'^(\w+)\s*=\s*', line.strip())
            if m and not line.strip().endswith(':'):
                name = m.group(1)
                assign_counts[name] = assign_counts.get(name, 0) + 1

        for line in tac:
            match = assign_pattern.match(line.strip())
            if match:
                name = match.group(1)
                value = match.group(2)
                # Only propagate if assigned exactly once
                if assign_counts.get(name, 0) == 1:
                    constants[name] = value

        # Second pass: substitute constants in expressions
        for line in tac:
            original_line = line
            stripped = line.strip()

            # Don't substitute in labels, gotos, or the assignment itself
            if stripped.endswith(':') or stripped.startswith('goto ') or stripped.startswith('nop'):
                result.append(line)
                continue

            # For assignments and expressions, substitute RHS only
            eq_match = re.match(r'^(\w+)\s*=\s*(.+)$', stripped)
            if eq_match:
                dest = eq_match.group(1)
                rhs = eq_match.group(2)
                new_rhs = self._substitute_constants(rhs, constants, dest)
                if new_rhs != rhs:
                    new_line = f"{dest} = {new_rhs}"
                    result.append(new_line)
                    changes.append(f"Constant propagation: {stripped} --> {new_line}")
                    continue

            # For print, iffalse, etc.
            if stripped.startswith('print '):
                val = stripped[6:]
                new_val = self._substitute_constants(val, constants)
                if new_val != val:
                    new_line = f"print {new_val}"
                    result.append(new_line)
                    changes.append(f"Constant propagation: {stripped} --> {new_line}")
                    continue

            if stripped.startswith('iffalse '):
                parts = stripped.split()
                if len(parts) >= 4:
                    cond = parts[1]
                    if cond in constants:
                        new_line = f"iffalse {constants[cond]} {' '.join(parts[2:])}"
                        result.append(new_line)
                        changes.append(f"Constant propagation: {stripped} --> {new_line}")
                        continue

            result.append(line)

        return result, changes

    def _substitute_constants(self, expr: str, constants: Dict[str, str], exclude: str = "") -> str:
        """Replace variable names with their constant values in an expression."""
        # Tokenize the expression simply
        tokens = re.findall(r'"[^"]*"|\w+|[+\-*/><]=?|==|!=', expr)
        new_tokens = []
        for tok in tokens:
            if tok in constants and tok != exclude and not tok.startswith('"'):
                new_tokens.append(constants[tok])
            else:
                new_tokens.append(tok)
        return " ".join(new_tokens)

    # ═══════════════════════════════════════════
    # Pass 3: Dead Code Elimination
    # ═══════════════════════════════════════════

    def _dead_code_elimination(self, tac: List[str]) -> tuple[List[str], List[str]]:
        """Remove assignments to temp variables that are never used elsewhere."""
        changes: List[str] = []

        # Collect all temp variable assignments (t0, t1, ...)
        temp_pattern = re.compile(r'^(t\d+)\s*=')

        # Find all references to each temp
        all_text = "\n".join(tac)
        used_temps: Set[str] = set()

        for line in tac:
            stripped = line.strip()
            m = temp_pattern.match(stripped)
            assigned_temp = m.group(1) if m else None

            # Find all temp references in this line (excluding the LHS assignment)
            refs = re.findall(r'\bt\d+\b', stripped)
            for ref in refs:
                if ref != assigned_temp:
                    used_temps.add(ref)

            # Also check iffalse, print, etc.
            if stripped.startswith('print ') or stripped.startswith('iffalse '):
                refs2 = re.findall(r'\bt\d+\b', stripped)
                used_temps.update(refs2)

        # Filter out dead assignments
        result: List[str] = []
        for line in tac:
            stripped = line.strip()
            m = temp_pattern.match(stripped)
            if m:
                temp_name = m.group(1)
                if temp_name not in used_temps:
                    changes.append(f"Dead code elimination: removed '{stripped}' (unused temp)")
                    continue
            result.append(line)

        return result, changes
