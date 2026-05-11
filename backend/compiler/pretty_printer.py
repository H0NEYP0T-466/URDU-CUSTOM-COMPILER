"""
Urdu Custom Compiler — Pretty Printer
Beautiful terminal output for Lexer tokens and Parser AST.
Uses ANSI colors and box-drawing characters for a polished look.
"""

from typing import List
from .lexer import Token, TokenType
from .parser import (
    ASTNode, NumberNode, StringNode, BoolNode, VarNode,
    BinOpNode, UnaryOpNode, AssignNode, PrintNode, IfNode, WhileNode,
    FuncDefNode, ReturnNode, FuncCallNode,
    ArrayLiteralNode, ArrayAccessNode, ArrayAssignNode,
    InputNode, TypeCastNode,
)


# ═══════════════════════════════════════════════
# ANSI Color Codes
# ═══════════════════════════════════════════════

class Colors:
    RESET      = "\033[0m"
    BOLD       = "\033[1m"
    DIM        = "\033[2m"
    ITALIC     = "\033[3m"
    UNDERLINE  = "\033[4m"

    # Foreground
    BLACK      = "\033[30m"
    RED        = "\033[31m"
    GREEN      = "\033[32m"
    YELLOW     = "\033[33m"
    BLUE       = "\033[34m"
    MAGENTA    = "\033[35m"
    CYAN       = "\033[36m"
    WHITE      = "\033[37m"

    # Bright foreground
    BR_RED     = "\033[91m"
    BR_GREEN   = "\033[92m"
    BR_YELLOW  = "\033[93m"
    BR_BLUE    = "\033[94m"
    BR_MAGENTA = "\033[95m"
    BR_CYAN    = "\033[96m"
    BR_WHITE   = "\033[97m"

    # Background
    BG_BLACK   = "\033[40m"
    BG_BLUE    = "\033[44m"
    BG_CYAN    = "\033[46m"
    BG_GREEN   = "\033[42m"
    BG_MAGENTA = "\033[45m"


C = Colors


# ═══════════════════════════════════════════════
# Token Table Printer
# ═══════════════════════════════════════════════

def print_tokens(tokens: List[Token]) -> None:
    """Print a beautiful table of lexer tokens to the terminal."""

    # Header banner
    print()
    print(f"  {C.BG_CYAN}{C.BLACK}{C.BOLD}  ⚡ LEXER OUTPUT — TOKEN TABLE  {C.RESET}")
    print()

    # Column widths
    idx_w = 5
    type_w = 14
    value_w = 22
    line_w = 6

    # Top border
    print(f"  {C.DIM}╔{'═' * idx_w}╤{'═' * type_w}╤{'═' * value_w}╤{'═' * line_w}╗{C.RESET}")

    # Header row
    print(
        f"  {C.DIM}║{C.RESET}"
        f"{C.BOLD}{C.BR_WHITE} {'#':^{idx_w - 1}}{C.RESET}"
        f"{C.DIM}│{C.RESET}"
        f"{C.BOLD}{C.BR_WHITE} {'TYPE':<{type_w - 1}}{C.RESET}"
        f"{C.DIM}│{C.RESET}"
        f"{C.BOLD}{C.BR_WHITE} {'VALUE':<{value_w - 1}}{C.RESET}"
        f"{C.DIM}│{C.RESET}"
        f"{C.BOLD}{C.BR_WHITE} {'LINE':^{line_w - 1}}{C.RESET}"
        f"{C.DIM}║{C.RESET}"
    )

    # Separator
    print(f"  {C.DIM}╟{'─' * idx_w}┼{'─' * type_w}┼{'─' * value_w}┼{'─' * line_w}╢{C.RESET}")

    # Token rows
    for i, token in enumerate(tokens):
        if token.type == TokenType.EOF:
            continue
        if token.type == TokenType.NEWLINE:
            continue

        # Color code by token type
        color = _token_color(token.type)

        # Format value (truncate if too long)
        val_display = repr(token.value)
        if len(val_display) > value_w - 2:
            val_display = val_display[: value_w - 5] + "..."

        type_name = token.type.name

        print(
            f"  {C.DIM}║{C.RESET}"
            f" {C.DIM}{i:>{idx_w - 2}} {C.RESET}"
            f"{C.DIM}│{C.RESET}"
            f" {color}{type_name:<{type_w - 2}} {C.RESET}"
            f"{C.DIM}│{C.RESET}"
            f" {C.BR_WHITE}{val_display:<{value_w - 2}} {C.RESET}"
            f"{C.DIM}│{C.RESET}"
            f" {C.DIM}{token.line:^{line_w - 2}} {C.RESET}"
            f"{C.DIM}║{C.RESET}"
        )

    # Bottom border
    print(f"  {C.DIM}╚{'═' * idx_w}╧{'═' * type_w}╧{'═' * value_w}╧{'═' * line_w}╝{C.RESET}")

    # Count summary
    real_tokens = [t for t in tokens if t.type not in (TokenType.EOF, TokenType.NEWLINE)]
    print(f"  {C.DIM}  Total tokens: {C.BR_CYAN}{len(real_tokens)}{C.RESET}")
    print()


def _token_color(token_type: TokenType) -> str:
    """Return ANSI color for a given token type."""
    return {
        TokenType.KEYWORD:    C.BR_CYAN + C.BOLD,
        TokenType.IDENTIFIER: C.BR_BLUE,
        TokenType.NUMBER:     C.BR_GREEN,
        TokenType.FLOAT:      C.BR_GREEN,
        TokenType.STRING:     C.BR_YELLOW,
        TokenType.OPERATOR:   C.BR_MAGENTA,
        TokenType.ASSIGN:     C.BR_RED,
        TokenType.LPAREN:     C.DIM,
        TokenType.RPAREN:     C.DIM,
        TokenType.COMMA:      C.DIM,
        TokenType.LBRACKET:   C.BR_YELLOW,
        TokenType.RBRACKET:   C.BR_YELLOW,
        TokenType.NEWLINE:    C.DIM,
        TokenType.EOF:        C.DIM,
    }.get(token_type, C.WHITE)


# ═══════════════════════════════════════════════
# AST Tree Printer
# ═══════════════════════════════════════════════

def print_ast(nodes: List[ASTNode]) -> None:
    """Print a beautiful tree visualization of the AST."""

    print(f"  {C.BG_MAGENTA}{C.BLACK}{C.BOLD}  🌳 PARSER OUTPUT — AST TREE  {C.RESET}")
    print()

    if not nodes:
        print(f"  {C.DIM}(empty program){C.RESET}")
        print()
        return

    for i, node in enumerate(nodes):
        is_last = (i == len(nodes) - 1)
        _print_node(node, prefix="  ", is_last=is_last)

    # Summary
    count = _count_nodes(nodes)
    print()
    print(f"  {C.DIM}  Total AST nodes: {C.BR_MAGENTA}{count}{C.RESET}")
    print()


def _print_node(node: ASTNode, prefix: str = "", is_last: bool = True) -> None:
    """Recursively print a single AST node with tree connectors."""

    connector = "└── " if is_last else "├── "
    child_prefix = prefix + ("    " if is_last else "│   ")

    if isinstance(node, AssignNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_RED}{C.BOLD}ASSIGN{C.RESET} {C.BR_BLUE}{node.name}{C.RESET} {C.DIM}={C.RESET}")
        _print_node(node.value_expr, child_prefix, is_last=True)

    elif isinstance(node, PrintNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_YELLOW}{C.BOLD}PRINT{C.RESET}")
        _print_node(node.expr, child_prefix, is_last=True)

    elif isinstance(node, IfNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_CYAN}{C.BOLD}IF{C.RESET}")
        # Condition
        print(f"{child_prefix}{C.DIM}├── {C.RESET}{C.ITALIC}{C.DIM}condition:{C.RESET}")
        _print_node(node.condition, child_prefix + "│   ", is_last=True)
        # Body
        if node.else_body:
            print(f"{child_prefix}{C.DIM}├── {C.RESET}{C.ITALIC}{C.DIM}then ({len(node.body)} stmts):{C.RESET}")
            for j, stmt in enumerate(node.body):
                _print_node(stmt, child_prefix + "│   ", is_last=(j == len(node.body) - 1))
            print(f"{child_prefix}{C.DIM}└── {C.RESET}{C.ITALIC}{C.DIM}else ({len(node.else_body)} stmts):{C.RESET}")
            for j, stmt in enumerate(node.else_body):
                _print_node(stmt, child_prefix + "    ", is_last=(j == len(node.else_body) - 1))
        else:
            print(f"{child_prefix}{C.DIM}└── {C.RESET}{C.ITALIC}{C.DIM}then ({len(node.body)} stmts):{C.RESET}")
            for j, stmt in enumerate(node.body):
                _print_node(stmt, child_prefix + "    ", is_last=(j == len(node.body) - 1))

    elif isinstance(node, WhileNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_GREEN}{C.BOLD}WHILE{C.RESET}")
        print(f"{child_prefix}{C.DIM}├── {C.RESET}{C.ITALIC}{C.DIM}condition:{C.RESET}")
        _print_node(node.condition, child_prefix + "│   ", is_last=True)
        print(f"{child_prefix}{C.DIM}└── {C.RESET}{C.ITALIC}{C.DIM}body ({len(node.body)} stmts):{C.RESET}")
        for j, stmt in enumerate(node.body):
            _print_node(stmt, child_prefix + "    ", is_last=(j == len(node.body) - 1))

    elif isinstance(node, BinOpNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_MAGENTA}BINOP{C.RESET} {C.BOLD}{C.BR_WHITE}[{node.op}]{C.RESET}")
        _print_node(node.left, child_prefix, is_last=False)
        _print_node(node.right, child_prefix, is_last=True)

    elif isinstance(node, UnaryOpNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_MAGENTA}UNARY{C.RESET} {C.BOLD}{C.BR_WHITE}[{node.op}]{C.RESET}")
        _print_node(node.operand, child_prefix, is_last=True)

    elif isinstance(node, NumberNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_GREEN}NUM{C.RESET} {C.BR_WHITE}{node.value}{C.RESET}")

    elif isinstance(node, StringNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_YELLOW}STR{C.RESET} {C.BR_WHITE}\"{node.value}\"{C.RESET}")

    elif isinstance(node, BoolNode):
        val = "sahi" if node.value else "ghalat"
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_CYAN}BOOL{C.RESET} {C.BR_WHITE}{val}{C.RESET}")

    elif isinstance(node, VarNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_BLUE}VAR{C.RESET} {C.BR_WHITE}{node.name}{C.RESET}")

    elif isinstance(node, FuncDefNode):
        params_str = ", ".join(node.params) if node.params else "(no params)"
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_CYAN}{C.BOLD}FUNC_DEF{C.RESET} {C.BR_BLUE}{node.name}{C.RESET} {C.DIM}({params_str}){C.RESET}")
        print(f"{child_prefix}{C.DIM}└── {C.RESET}{C.ITALIC}{C.DIM}body ({len(node.body)} stmts):{C.RESET}")
        for j, stmt in enumerate(node.body):
            _print_node(stmt, child_prefix + "    ", is_last=(j == len(node.body) - 1))

    elif isinstance(node, ReturnNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_RED}{C.BOLD}RETURN{C.RESET}")
        if node.value:
            _print_node(node.value, child_prefix, is_last=True)

    elif isinstance(node, FuncCallNode):
        args_str = f"{len(node.args)} args" if node.args else "no args"
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_GREEN}{C.BOLD}CALL{C.RESET} {C.BR_BLUE}{node.name}{C.RESET} {C.DIM}({args_str}){C.RESET}")
        for j, arg in enumerate(node.args):
            _print_node(arg, child_prefix, is_last=(j == len(node.args) - 1))

    elif isinstance(node, ArrayLiteralNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_YELLOW}{C.BOLD}ARRAY{C.RESET} {C.DIM}[{len(node.elements)} elements]{C.RESET}")
        for j, elem in enumerate(node.elements):
            _print_node(elem, child_prefix, is_last=(j == len(node.elements) - 1))

    elif isinstance(node, ArrayAccessNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_YELLOW}INDEX_ACCESS{C.RESET}")
        _print_node(node.array, child_prefix, is_last=False)
        print(f"{child_prefix}{C.DIM}└── {C.RESET}{C.ITALIC}{C.DIM}index:{C.RESET}")
        _print_node(node.index, child_prefix + "    ", is_last=True)

    elif isinstance(node, ArrayAssignNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_RED}{C.BOLD}ARRAY_ASSIGN{C.RESET} {C.BR_BLUE}{node.name}{C.RESET}")
        print(f"{child_prefix}{C.DIM}├── {C.RESET}{C.ITALIC}{C.DIM}index:{C.RESET}")
        _print_node(node.index, child_prefix + "│   ", is_last=True)
        print(f"{child_prefix}{C.DIM}└── {C.RESET}{C.ITALIC}{C.DIM}value:{C.RESET}")
        _print_node(node.value, child_prefix + "    ", is_last=True)

    elif isinstance(node, InputNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_GREEN}INPUT{C.RESET}")
        if node.prompt:
            _print_node(node.prompt, child_prefix, is_last=True)

    elif isinstance(node, TypeCastNode):
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.BR_MAGENTA}CAST{C.RESET} {C.BR_WHITE}{node.target_type}(){C.RESET}")
        _print_node(node.expr, child_prefix, is_last=True)

    else:
        print(f"{prefix}{C.DIM}{connector}{C.RESET}{C.RED}UNKNOWN{C.RESET} {type(node).__name__}")


def _count_nodes(nodes: List[ASTNode]) -> int:
    """Count total number of AST nodes recursively."""
    count = 0
    for node in nodes:
        count += 1
        if isinstance(node, AssignNode):
            count += _count_nodes([node.value_expr])
        elif isinstance(node, PrintNode):
            count += _count_nodes([node.expr])
        elif isinstance(node, IfNode):
            count += _count_nodes([node.condition])
            count += _count_nodes(node.body)
            count += _count_nodes(node.else_body)
        elif isinstance(node, WhileNode):
            count += _count_nodes([node.condition])
            count += _count_nodes(node.body)
        elif isinstance(node, BinOpNode):
            count += _count_nodes([node.left, node.right])
        elif isinstance(node, UnaryOpNode):
            count += _count_nodes([node.operand])
        elif isinstance(node, FuncDefNode):
            count += _count_nodes(node.body)
        elif isinstance(node, ReturnNode):
            if node.value:
                count += _count_nodes([node.value])
        elif isinstance(node, FuncCallNode):
            count += _count_nodes(node.args)
        elif isinstance(node, ArrayLiteralNode):
            count += _count_nodes(node.elements)
        elif isinstance(node, ArrayAccessNode):
            count += _count_nodes([node.array, node.index])
        elif isinstance(node, ArrayAssignNode):
            count += _count_nodes([node.index, node.value])
        elif isinstance(node, InputNode):
            if node.prompt:
                count += _count_nodes([node.prompt])
        elif isinstance(node, TypeCastNode):
            count += _count_nodes([node.expr])
    return count


# ═══════════════════════════════════════════════
# Execution Result Printer
# ═══════════════════════════════════════════════

def print_execution_result(output_lines: List[str], exec_time_ms: float) -> None:
    """Print the interpreter output beautifully."""

    print(f"  {C.BG_GREEN}{C.BLACK}{C.BOLD}  ▶ INTERPRETER OUTPUT  {C.RESET}")
    print()

    if output_lines:
        for line in output_lines:
            print(f"  {C.BR_GREEN}  ❯ {line}{C.RESET}")
    else:
        print(f"  {C.DIM}  (no output){C.RESET}")

    print()
    print(f"  {C.DIM}  ⏱  Execution time: {C.BR_GREEN}{exec_time_ms:.2f}ms{C.RESET}")
    print()


def print_error(error_msg: str, stage: str) -> None:
    """Print an error message beautifully."""

    print()
    print(f"  {C.BG_BLACK}{C.BR_RED}{C.BOLD}  ❌ {stage} ERROR  {C.RESET}")
    print(f"  {C.BR_RED}  {error_msg}{C.RESET}")
    print()


def print_separator() -> None:
    """Print a visual separator between pipeline stages."""
    print(f"  {C.DIM}{'─' * 52}{C.RESET}")
