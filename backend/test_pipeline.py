"""Quick test of the full compiler pipeline."""
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer
from compiler.ir_generator import IRGenerator
from compiler.optimizer import Optimizer
from compiler.codegen import CodeGenerator
from compiler.interpreter import Interpreter

code = """rakho x = 10
rakho y = 3
agar x > y
    dikhao "x bara hai"
warna
    dikhao "y bara hai"
khatam
jabtak x > 0
    dikhao x
    rakho x = x - 1
khatam
"""

print("=== LEXER ===")
tokens = Lexer(code).tokenize()
for t in tokens:
    if t.type.name not in ("NEWLINE", "EOF"):
        print(f"  {t}")

print("\n=== PARSER ===")
ast = Parser(tokens).parse()
print(f"  {len(ast)} top-level nodes")

print("\n=== SEMANTIC ===")
sem = SemanticAnalyzer().analyze(ast)
print(f"  Errors: {sem.errors}")
print(f"  Warnings: {sem.warnings}")
print(f"  Symbol Table: {sem.symbol_table}")

print("\n=== TAC ===")
tac = IRGenerator().generate(ast)
for i, instr in enumerate(tac):
    print(f"  {i:>3}  {instr}")

print("\n=== OPTIMIZER ===")
opt = Optimizer().optimize(tac)
print(f"  Changes: {opt.changes}")
for i, instr in enumerate(opt.optimized):
    print(f"  {i:>3}  {instr}")

print("\n=== CODEGEN ===")
pycode = CodeGenerator().generate(ast)
print(pycode)

print("\n=== INTERPRETER ===")
output = Interpreter().execute(ast)
for line in output:
    print(f"  > {line}")

print("\nAll phases passed!")
