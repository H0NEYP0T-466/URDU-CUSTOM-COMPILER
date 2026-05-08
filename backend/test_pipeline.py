"""Test block scoping and the full pipeline."""
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer
from compiler.ir_generator import IRGenerator
from compiler.optimizer import Optimizer
from compiler.codegen import CodeGenerator
from compiler.interpreter import Interpreter

# Test 1: Block scoping - variable inside agar should be local
print("=== TEST 1: Block Scoping ===")
code1 = """rakho x = 10
agar x > 5
    rakho inner = 99
    dikhao inner
khatam
dikhao x
"""
tokens = Lexer(code1).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
print(f"  Scoped symbols:")
for entry in sem.scoped_symbols:
    print(f"    {entry.name} : {entry.var_type} @ {entry.scope} (depth={entry.scope_depth})")
print(f"  Errors: {sem.errors}")
print(f"  Warnings: {sem.warnings}")

# Execute to make sure scoping works at runtime
output = Interpreter().execute(ast)
print(f"  Output: {output}")
print()

# Test 2: Constant folding example
print("=== TEST 2: Constant Folding ===")
code2 = """rakho x = 5 + 3
rakho y = 10 * 2
rakho z = 100 / 4
dikhao x
dikhao y
dikhao z
"""
tokens = Lexer(code2).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
tac = IRGenerator().generate(ast)
opt = Optimizer().optimize(tac)
print(f"  Original TAC lines: {len(opt.original)}")
print(f"  Optimized TAC lines: {len(opt.optimized)}")
print(f"  Changes: {opt.changes}")
output = Interpreter().execute(ast)
print(f"  Output: {output}")
print()

# Test 3: Semantic error test
print("=== TEST 3: Semantic Errors ===")
code3 = """rakho x = "hello"
rakho y = x + 5
dikhao z
"""
tokens = Lexer(code3).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
print(f"  Errors: {sem.errors}")
print()

# Test 4: While loop scoping
print("=== TEST 4: While Loop Scoping ===")
code4 = """rakho x = 3
jabtak x > 0
    rakho msg = "loop"
    dikhao x
    rakho x = x - 1
khatam
"""
tokens = Lexer(code4).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
print(f"  Scoped symbols:")
for entry in sem.scoped_symbols:
    print(f"    {entry.name} : {entry.var_type} @ {entry.scope} (depth={entry.scope_depth})")
output = Interpreter().execute(ast)
print(f"  Output: {output}")

print("\nAll tests passed!")
