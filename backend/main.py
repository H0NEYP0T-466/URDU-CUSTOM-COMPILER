"""
Urdu Custom Compiler - FastAPI Backend
Single endpoint: POST /run
Full pipeline: Lexer -> Parser -> Semantic -> IR -> Optimizer -> CodeGen -> Interpreter
Prints beautiful terminal output for every stage including scoped symbol table.
"""

import re
import time
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from compiler.lexer import Lexer, LexError, TokenType
from compiler.parser import Parser, ParseError
from compiler.semantic import SemanticAnalyzer
from compiler.ir_generator import IRGenerator
from compiler.optimizer import Optimizer
from compiler.codegen import CodeGenerator
from compiler.interpreter import Interpreter, UrduRuntimeError
from compiler.pretty_printer import (
    print_tokens,
    print_ast,
    print_execution_result,
    print_error,
    print_separator,
    Colors as C,
)

app = FastAPI(
    title="Urdu Custom Compiler",
    description="A Roman-Urdu programming language interpreter",
    version="2.1.0",
)

# CORS -- allow all origins for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -- Request / Response Models --

class RunRequest(BaseModel):
    code: str


class TokenInfo(BaseModel):
    index: int
    type: str
    value: str
    line: int


class SymbolEntryInfo(BaseModel):
    name: str
    var_type: str
    scope: str
    scope_depth: int


class SemanticInfo(BaseModel):
    errors: list[str]
    warnings: list[str]
    symbol_table: dict[str, str]
    scoped_symbols: list[SymbolEntryInfo] = []


class TACInfo(BaseModel):
    original: list[str]
    optimized: list[str]
    changes: list[str]


class ErrorMarker(BaseModel):
    line: int
    message: str
    severity: str   # "error" | "warning"


class RunResponse(BaseModel):
    output: str
    error: Optional[str] = None
    error_line: Optional[int] = None
    error_markers: list[ErrorMarker] = []
    tokens: list[TokenInfo] = []
    ast: str = ""
    semantic: Optional[SemanticInfo] = None
    tac: Optional[TACInfo] = None
    generated_python: str = ""


# -- Helpers --

def extract_line_from_error(error_str: str) -> Optional[int]:
    """Extract a line number from error messages like 'Parser Ghalati (line 5): ...'"""
    match = re.search(r'\(line (\d+)\)', error_str)
    if match:
        return int(match.group(1))
    return None


def ast_to_string(nodes: list, indent: int = 0) -> str:
    """Convert AST nodes to a readable tree string for the frontend."""
    from compiler.parser import (
        AssignNode, PrintNode, IfNode, WhileNode,
        BinOpNode, UnaryOpNode, NumberNode, StringNode, BoolNode, VarNode,
    )

    lines: list[str] = []
    prefix = "  " * indent

    for node in nodes:
        if isinstance(node, AssignNode):
            lines.append(f"{prefix}ASSIGN {node.name} =")
            lines.append(ast_to_string([node.value_expr], indent + 1))
        elif isinstance(node, PrintNode):
            lines.append(f"{prefix}PRINT")
            lines.append(ast_to_string([node.expr], indent + 1))
        elif isinstance(node, IfNode):
            lines.append(f"{prefix}IF")
            lines.append(f"{prefix}  condition:")
            lines.append(ast_to_string([node.condition], indent + 2))
            lines.append(f"{prefix}  then ({len(node.body)} stmts):")
            lines.append(ast_to_string(node.body, indent + 2))
            if node.else_body:
                lines.append(f"{prefix}  else ({len(node.else_body)} stmts):")
                lines.append(ast_to_string(node.else_body, indent + 2))
        elif isinstance(node, WhileNode):
            lines.append(f"{prefix}WHILE")
            lines.append(f"{prefix}  condition:")
            lines.append(ast_to_string([node.condition], indent + 2))
            lines.append(f"{prefix}  body ({len(node.body)} stmts):")
            lines.append(ast_to_string(node.body, indent + 2))
        elif isinstance(node, BinOpNode):
            lines.append(f"{prefix}BINOP [{node.op}]")
            lines.append(ast_to_string([node.left], indent + 1))
            lines.append(ast_to_string([node.right], indent + 1))
        elif isinstance(node, UnaryOpNode):
            lines.append(f"{prefix}UNARY [{node.op}]")
            lines.append(ast_to_string([node.operand], indent + 1))
        elif isinstance(node, NumberNode):
            lines.append(f"{prefix}NUM {node.value}")
        elif isinstance(node, StringNode):
            lines.append(f'{prefix}STR "{node.value}"')
        elif isinstance(node, BoolNode):
            lines.append(f"{prefix}BOOL {'sahi' if node.value else 'ghalat'}")
        elif isinstance(node, VarNode):
            lines.append(f"{prefix}VAR {node.name}")

    return "\n".join(lines)


def print_symbol_table(sem_result) -> None:
    """Print a beautiful scoped symbol table to the terminal."""
    if not sem_result.scoped_symbols:
        return

    print()
    print(f"  {C.BG_CYAN}{C.BLACK}{C.BOLD}  SYMBOL TABLE  {C.RESET}")
    print()

    # Table header
    print(f"    {C.DIM}+{'-'*20}+{'-'*12}+{'-'*22}+{'-'*8}+{C.RESET}")
    print(f"    {C.DIM}|{C.RESET} {C.BOLD}{'Variable':<18}{C.RESET} {C.DIM}|{C.RESET} {C.BOLD}{'Type':<10}{C.RESET} {C.DIM}|{C.RESET} {C.BOLD}{'Scope':<20}{C.RESET} {C.DIM}|{C.RESET} {C.BOLD}{'Depth':<6}{C.RESET} {C.DIM}|{C.RESET}")
    print(f"    {C.DIM}+{'-'*20}+{'-'*12}+{'-'*22}+{'-'*8}+{C.RESET}")

    for entry in sem_result.scoped_symbols:
        # Color based on scope depth
        if entry.scope_depth == 0:
            scope_color = C.BR_GREEN
        elif entry.scope_depth == 1:
            scope_color = C.BR_YELLOW
        else:
            scope_color = C.BR_MAGENTA

        depth_indicator = "  " * entry.scope_depth + str(entry.scope_depth)

        print(
            f"    {C.DIM}|{C.RESET} {C.BR_BLUE}{entry.name:<18}{C.RESET} "
            f"{C.DIM}|{C.RESET} {C.BR_CYAN}{entry.var_type:<10}{C.RESET} "
            f"{C.DIM}|{C.RESET} {scope_color}{entry.scope:<20}{C.RESET} "
            f"{C.DIM}|{C.RESET} {scope_color}{depth_indicator:<6}{C.RESET} {C.DIM}|{C.RESET}"
        )

    print(f"    {C.DIM}+{'-'*20}+{'-'*12}+{'-'*22}+{'-'*8}+{C.RESET}")
    print()


@app.post("/run", response_model=RunResponse)
async def run_code(request: RunRequest) -> RunResponse:
    """Execute Urdu code through the full compiler pipeline."""
    code = request.code

    if not code.strip():
        return RunResponse(output="")

    # -- Banner --
    print()
    print(f"  {C.BG_BLUE}{C.BR_WHITE}{C.BOLD}  =============================================  {C.RESET}")
    print(f"  {C.BG_BLUE}{C.BR_WHITE}{C.BOLD}    URDU-CUSTOM-COMPILER -- New Request          {C.RESET}")
    print(f"  {C.BG_BLUE}{C.BR_WHITE}{C.BOLD}  =============================================  {C.RESET}")
    print()

    # Show source code
    print(f"  {C.DIM}+-- Source Code ------------------------------------------{C.RESET}")
    for i, line in enumerate(code.splitlines(), 1):
        print(f"  {C.DIM}|{C.RESET} {C.DIM}{i:>3} |{C.RESET} {C.BR_WHITE}{line}{C.RESET}")
    print(f"  {C.DIM}+--------------------------------------------------------{C.RESET}")
    print()

    # Accumulate response data
    token_list: list[TokenInfo] = []
    ast_str = ""
    semantic_info: Optional[SemanticInfo] = None
    tac_info: Optional[TACInfo] = None
    generated_python = ""
    error_markers: list[ErrorMarker] = []

    try:
        # === Stage 1: Lexing ===
        start = time.perf_counter()
        tokens = Lexer(code).tokenize()
        lex_time = (time.perf_counter() - start) * 1000

        # Build token list for response
        idx = 0
        for tok in tokens:
            if tok.type in (TokenType.EOF, TokenType.NEWLINE):
                continue
            token_list.append(TokenInfo(
                index=idx, type=tok.type.name, value=tok.value, line=tok.line
            ))
            idx += 1

        print_tokens(tokens)
        print(f"  {C.DIM}  >> Lexer time: {C.BR_CYAN}{lex_time:.2f}ms{C.RESET}")
        print_separator()

        # === Stage 2: Parsing ===
        start = time.perf_counter()
        ast = Parser(tokens).parse()
        parse_time = (time.perf_counter() - start) * 1000

        ast_str = ast_to_string(ast)

        print_ast(ast)
        print(f"  {C.DIM}  >> Parser time: {C.BR_MAGENTA}{parse_time:.2f}ms{C.RESET}")
        print_separator()

        # === Stage 3: Semantic Analysis ===
        start = time.perf_counter()
        sem_result = SemanticAnalyzer().analyze(ast)
        sem_time = (time.perf_counter() - start) * 1000

        # Build scoped symbols for response
        scoped_entries = [
            SymbolEntryInfo(
                name=e.name, var_type=e.var_type,
                scope=e.scope, scope_depth=e.scope_depth,
            )
            for e in sem_result.scoped_symbols
        ]

        semantic_info = SemanticInfo(
            errors=sem_result.errors,
            warnings=sem_result.warnings,
            symbol_table=sem_result.symbol_table,
            scoped_symbols=scoped_entries,
        )

        # Build error markers from semantic warnings/errors
        for w in sem_result.warnings:
            error_markers.append(ErrorMarker(line=1, message=w, severity="warning"))
        for e in sem_result.errors:
            error_markers.append(ErrorMarker(line=1, message=e, severity="error"))

        # Print semantic results to terminal
        print(f"  {C.BG_CYAN}{C.BLACK}{C.BOLD}  SEMANTIC ANALYSIS  {C.RESET}")
        print()

        # Print the scoped symbol table
        print_symbol_table(sem_result)

        if sem_result.warnings:
            for w in sem_result.warnings:
                print(f"  {C.BR_YELLOW}  ! {w}{C.RESET}")
        if sem_result.errors:
            for e in sem_result.errors:
                print(f"  {C.BR_RED}  X {e}{C.RESET}")
            print(f"  {C.DIM}  >> Semantic time: {C.BR_CYAN}{sem_time:.2f}ms{C.RESET}")
            print_separator()
            # Return early with semantic errors
            return RunResponse(
                output="",
                error="Semantic Ghalati: " + "; ".join(sem_result.errors),
                error_line=1,
                error_markers=error_markers,
                tokens=token_list,
                ast=ast_str,
                semantic=semantic_info,
            )
        else:
            print(f"  {C.BR_GREEN}  [OK] Semantic check passed{C.RESET}")
        print(f"  {C.DIM}  >> Semantic time: {C.BR_CYAN}{sem_time:.2f}ms{C.RESET}")
        print_separator()

        # === Stage 4: IR Generation (TAC) ===
        start = time.perf_counter()
        tac_original = IRGenerator().generate(ast)
        ir_time = (time.perf_counter() - start) * 1000

        print(f"  {C.BG_MAGENTA}{C.BLACK}{C.BOLD}  TAC -- Three Address Code  {C.RESET}")
        print()
        for i, instr in enumerate(tac_original):
            print(f"    {C.DIM}{i:>3}{C.RESET}  {C.BR_WHITE}{instr}{C.RESET}")
        print(f"  {C.DIM}  >> IR generation time: {C.BR_MAGENTA}{ir_time:.2f}ms{C.RESET}")
        print_separator()

        # === Stage 5: Optimization ===
        start = time.perf_counter()
        opt_result = Optimizer().optimize(tac_original)
        opt_time = (time.perf_counter() - start) * 1000

        tac_info = TACInfo(
            original=opt_result.original,
            optimized=opt_result.optimized,
            changes=opt_result.changes,
        )

        print(f"  {C.BG_GREEN}{C.BLACK}{C.BOLD}  OPTIMIZATION  {C.RESET}")
        print()
        for change in opt_result.changes:
            print(f"    {C.BR_YELLOW}-> {change}{C.RESET}")
        print(f"  {C.DIM}  >> Optimization time: {C.BR_GREEN}{opt_time:.2f}ms{C.RESET}")
        print_separator()

        # === Stage 6: Python Code Generation ===
        start = time.perf_counter()
        generated_python = CodeGenerator().generate(ast)
        codegen_time = (time.perf_counter() - start) * 1000

        print(f"  {C.BG_BLUE}{C.BR_WHITE}{C.BOLD}  GENERATED PYTHON  {C.RESET}")
        print()
        for line in generated_python.splitlines():
            print(f"    {C.BR_GREEN}{line}{C.RESET}")
        print(f"  {C.DIM}  >> Code generation time: {C.BR_BLUE}{codegen_time:.2f}ms{C.RESET}")
        print_separator()

        # === Stage 7: Interpretation ===
        start = time.perf_counter()
        interpreter = Interpreter()
        output_lines = interpreter.execute(ast)
        exec_time = (time.perf_counter() - start) * 1000

        print_execution_result(output_lines, exec_time)

        # -- Total time --
        total = lex_time + parse_time + sem_time + ir_time + opt_time + codegen_time + exec_time
        print(f"  {C.DIM}  Total pipeline: {C.BR_GREEN}{C.BOLD}{total:.2f}ms{C.RESET}")
        print()

        return RunResponse(
            output="\n".join(output_lines),
            error=None,
            tokens=token_list,
            ast=ast_str,
            semantic=semantic_info,
            tac=tac_info,
            generated_python=generated_python,
            error_markers=error_markers,
        )

    except LexError as e:
        err_str = str(e)
        err_line = extract_line_from_error(err_str)
        print_error(err_str, "LEXER")
        if err_line:
            error_markers.append(ErrorMarker(line=err_line, message=err_str, severity="error"))
        return RunResponse(
            output="", error=err_str, error_line=err_line,
            error_markers=error_markers, tokens=token_list,
        )
    except ParseError as e:
        err_str = str(e)
        err_line = e.line
        print_error(err_str, "PARSER")
        error_markers.append(ErrorMarker(line=err_line, message=err_str, severity="error"))
        return RunResponse(
            output="", error=err_str, error_line=err_line,
            error_markers=error_markers, tokens=token_list, ast=ast_str,
        )
    except UrduRuntimeError as e:
        err_str = str(e)
        print_error(err_str, "RUNTIME")
        return RunResponse(
            output="", error=err_str,
            error_markers=error_markers,
            tokens=token_list, ast=ast_str,
            semantic=semantic_info, tac=tac_info,
            generated_python=generated_python,
        )
    except Exception as e:
        err_str = str(e)
        print_error(err_str, "INTERNAL")
        return RunResponse(output="", error=f"Internal Error: {err_str}")


@app.get("/")
async def root():
    return {"message": "Urdu Custom Compiler API v2.1 -- POST /run to execute code"}
