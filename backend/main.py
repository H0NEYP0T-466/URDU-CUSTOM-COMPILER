"""
Urdu Custom Compiler - FastAPI Backend
Single endpoint: POST /run
Full pipeline: Lexer → Parser → Semantic → IR → Optimizer → CodeGen → Interpreter
Prints beautiful terminal output for every stage.
"""

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
    version="2.0.0",
)

# CORS — allow all origins for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response Models ──

class RunRequest(BaseModel):
    code: str


class TokenInfo(BaseModel):
    index: int
    type: str
    value: str
    line: int


class SemanticInfo(BaseModel):
    errors: list[str]
    warnings: list[str]
    symbol_table: dict[str, str]


class TACInfo(BaseModel):
    original: list[str]
    optimized: list[str]
    changes: list[str]


class RunResponse(BaseModel):
    output: str
    error: Optional[str] = None
    tokens: list[TokenInfo] = []
    ast: str = ""
    semantic: Optional[SemanticInfo] = None
    tac: Optional[TACInfo] = None
    generated_python: str = ""


# ── AST to string helper ──

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


@app.post("/run", response_model=RunResponse)
async def run_code(request: RunRequest) -> RunResponse:
    """Execute Urdu code through the full compiler pipeline."""
    code = request.code

    if not code.strip():
        return RunResponse(output="")

    # ── Banner ──
    print()
    print(f"  {C.BG_BLUE}{C.BR_WHITE}{C.BOLD}  ═══════════════════════════════════════════  {C.RESET}")
    print(f"  {C.BG_BLUE}{C.BR_WHITE}{C.BOLD}    🚀 URDU-CUSTOM-COMPILER — New Request     {C.RESET}")
    print(f"  {C.BG_BLUE}{C.BR_WHITE}{C.BOLD}  ═══════════════════════════════════════════  {C.RESET}")
    print()

    # Show source code
    print(f"  {C.DIM}┌─ Source Code ──────────────────────────────{C.RESET}")
    for i, line in enumerate(code.splitlines(), 1):
        print(f"  {C.DIM}│{C.RESET} {C.DIM}{i:>3} │{C.RESET} {C.BR_WHITE}{line}{C.RESET}")
    print(f"  {C.DIM}└────────────────────────────────────────────{C.RESET}")
    print()

    # Accumulate response data
    token_list: list[TokenInfo] = []
    ast_str = ""
    semantic_info: Optional[SemanticInfo] = None
    tac_info: Optional[TACInfo] = None
    generated_python = ""

    try:
        # ═══ Stage 1: Lexing ═══
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
        print(f"  {C.DIM}  ⏱  Lexer time: {C.BR_CYAN}{lex_time:.2f}ms{C.RESET}")
        print_separator()

        # ═══ Stage 2: Parsing ═══
        start = time.perf_counter()
        ast = Parser(tokens).parse()
        parse_time = (time.perf_counter() - start) * 1000

        ast_str = ast_to_string(ast)

        print_ast(ast)
        print(f"  {C.DIM}  ⏱  Parser time: {C.BR_MAGENTA}{parse_time:.2f}ms{C.RESET}")
        print_separator()

        # ═══ Stage 3: Semantic Analysis ═══
        start = time.perf_counter()
        sem_result = SemanticAnalyzer().analyze(ast)
        sem_time = (time.perf_counter() - start) * 1000

        semantic_info = SemanticInfo(
            errors=sem_result.errors,
            warnings=sem_result.warnings,
            symbol_table=sem_result.symbol_table,
        )

        # Print semantic results to terminal
        print(f"  {C.BG_CYAN}{C.BLACK}{C.BOLD}  🔍 SEMANTIC ANALYSIS  {C.RESET}")
        print()
        if sem_result.symbol_table:
            print(f"  {C.DIM}  Symbol Table:{C.RESET}")
            for var, typ in sem_result.symbol_table.items():
                print(f"    {C.BR_BLUE}{var}{C.RESET} : {C.BR_GREEN}{typ}{C.RESET}")
        if sem_result.warnings:
            for w in sem_result.warnings:
                print(f"  {C.BR_YELLOW}  ⚠ {w}{C.RESET}")
        if sem_result.errors:
            for e in sem_result.errors:
                print(f"  {C.BR_RED}  ✗ {e}{C.RESET}")
            print(f"  {C.DIM}  ⏱  Semantic time: {C.BR_CYAN}{sem_time:.2f}ms{C.RESET}")
            print_separator()
            # Return early with semantic errors
            return RunResponse(
                output="",
                error="Semantic Ghalati: " + "; ".join(sem_result.errors),
                tokens=token_list,
                ast=ast_str,
                semantic=semantic_info,
            )
        else:
            print(f"  {C.BR_GREEN}  ✓ Semantic check passed{C.RESET}")
        print(f"  {C.DIM}  ⏱  Semantic time: {C.BR_CYAN}{sem_time:.2f}ms{C.RESET}")
        print_separator()

        # ═══ Stage 4: IR Generation (TAC) ═══
        start = time.perf_counter()
        tac_original = IRGenerator().generate(ast)
        ir_time = (time.perf_counter() - start) * 1000

        print(f"  {C.BG_MAGENTA}{C.BLACK}{C.BOLD}  ⚡ TAC — Three Address Code  {C.RESET}")
        print()
        for i, instr in enumerate(tac_original):
            print(f"    {C.DIM}{i:>3}{C.RESET}  {C.BR_WHITE}{instr}{C.RESET}")
        print(f"  {C.DIM}  ⏱  IR generation time: {C.BR_MAGENTA}{ir_time:.2f}ms{C.RESET}")
        print_separator()

        # ═══ Stage 5: Optimization ═══
        start = time.perf_counter()
        opt_result = Optimizer().optimize(tac_original)
        opt_time = (time.perf_counter() - start) * 1000

        tac_info = TACInfo(
            original=opt_result.original,
            optimized=opt_result.optimized,
            changes=opt_result.changes,
        )

        print(f"  {C.BG_GREEN}{C.BLACK}{C.BOLD}  🔧 OPTIMIZATION  {C.RESET}")
        print()
        for change in opt_result.changes:
            print(f"    {C.BR_YELLOW}→ {change}{C.RESET}")
        print(f"  {C.DIM}  ⏱  Optimization time: {C.BR_GREEN}{opt_time:.2f}ms{C.RESET}")
        print_separator()

        # ═══ Stage 6: Python Code Generation ═══
        start = time.perf_counter()
        generated_python = CodeGenerator().generate(ast)
        codegen_time = (time.perf_counter() - start) * 1000

        print(f"  {C.BG_BLUE}{C.BR_WHITE}{C.BOLD}  🐍 GENERATED PYTHON  {C.RESET}")
        print()
        for line in generated_python.splitlines():
            print(f"    {C.BR_GREEN}{line}{C.RESET}")
        print(f"  {C.DIM}  ⏱  Code generation time: {C.BR_BLUE}{codegen_time:.2f}ms{C.RESET}")
        print_separator()

        # ═══ Stage 7: Interpretation ═══
        start = time.perf_counter()
        interpreter = Interpreter()
        output_lines = interpreter.execute(ast)
        exec_time = (time.perf_counter() - start) * 1000

        print_execution_result(output_lines, exec_time)

        # ── Total time ──
        total = lex_time + parse_time + sem_time + ir_time + opt_time + codegen_time + exec_time
        print(f"  {C.DIM}  📊 Total pipeline: {C.BR_GREEN}{C.BOLD}{total:.2f}ms{C.RESET}")
        print()

        return RunResponse(
            output="\n".join(output_lines),
            error=None,
            tokens=token_list,
            ast=ast_str,
            semantic=semantic_info,
            tac=tac_info,
            generated_python=generated_python,
        )

    except LexError as e:
        print_error(str(e), "LEXER")
        return RunResponse(output="", error=str(e), tokens=token_list)
    except ParseError as e:
        print_error(str(e), "PARSER")
        return RunResponse(output="", error=str(e), tokens=token_list, ast=ast_str)
    except UrduRuntimeError as e:
        print_error(str(e), "RUNTIME")
        return RunResponse(
            output="", error=str(e),
            tokens=token_list, ast=ast_str,
            semantic=semantic_info, tac=tac_info,
            generated_python=generated_python,
        )
    except Exception as e:
        print_error(str(e), "INTERNAL")
        return RunResponse(output="", error=f"Internal Error: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Urdu Custom Compiler API v2.0 — POST /run to execute code"}
