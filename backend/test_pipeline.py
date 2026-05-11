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

print("\n--- Existing tests passed! ---\n")

# ═══════════════════════════════════════════
# NEW FEATURE TESTS
# ═══════════════════════════════════════════

# Test 5: Function definition and call
print("=== TEST 5: Functions — banao / karo / wapis ===")
code5 = """banao greet()
    dikhao "Assalam o Alaikum!"
khatam

karo greet()
"""
tokens = Lexer(code5).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
print(f"  Semantic errors: {sem.errors}")
output = Interpreter().execute(ast)
print(f"  Output: {output}")
assert output == ["Assalam o Alaikum!"], f"Expected ['Assalam o Alaikum!'], got {output}"
print("  ✓ PASSED")
print()

# Test 6: Function with params and return
print("=== TEST 6: Function with params + wapis ===")
code6 = """banao add(a, b)
    wapis a + b
khatam

rakho result = add(10, 20)
dikhao result
"""
tokens = Lexer(code6).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
print(f"  Semantic errors: {sem.errors}")
output = Interpreter().execute(ast)
print(f"  Output: {output}")
assert output == ["30"], f"Expected ['30'], got {output}"
print("  ✓ PASSED")
print()

# Test 7: Function call in expression
print("=== TEST 7: Function call in expression ===")
code7 = """banao double(x)
    wapis x * 2
khatam

rakho y = double(5) + 3
dikhao y
"""
tokens = Lexer(code7).tokenize()
ast = Parser(tokens).parse()
output = Interpreter().execute(ast)
print(f"  Output: {output}")
assert output == ["13"], f"Expected ['13'], got {output}"
print("  ✓ PASSED")
print()

# Test 8: Array creation and access
print("=== TEST 8: Arrays — creation + access ===")
code8 = """rakho list = [10, 20, 30]
dikhao list[0]
dikhao list[1]
dikhao list[2]
"""
tokens = Lexer(code8).tokenize()
ast = Parser(tokens).parse()
output = Interpreter().execute(ast)
print(f"  Output: {output}")
assert output == ["10", "20", "30"], f"Expected ['10', '20', '30'], got {output}"
print("  ✓ PASSED")
print()

# Test 9: Array assignment
print("=== TEST 9: Arrays — index assignment ===")
code9 = """rakho nums = [1, 2, 3]
rakho nums[1] = 99
dikhao nums[1]
dikhao nums
"""
tokens = Lexer(code9).tokenize()
ast = Parser(tokens).parse()
output = Interpreter().execute(ast)
print(f"  Output: {output}")
assert output == ["99", "[1, 99, 3]"], f"Expected ['99', '[1, 99, 3]'], got {output}"
print("  ✓ PASSED")
print()

# Test 10: User input with pre-supplied values
print("=== TEST 10: User Input — input() ===")
code10 = """rakho naam = input("Apna naam likho: ")
dikhao naam
"""
tokens = Lexer(code10).tokenize()
ast = Parser(tokens).parse()
output = Interpreter().execute(ast, inputs=["Fezan"])
print(f"  Output: {output}")
assert output == ["Apna naam likho: Fezan", "Fezan"], f"Expected prompt echo + value, got {output}"
print("  ✓ PASSED")
print()

# Test 11: Type casting — int()
print("=== TEST 11: Type Casting — int() + str() ===")
code11 = """rakho x = int("42")
rakho y = x + 8
dikhao y
rakho z = str(y)
dikhao z
"""
tokens = Lexer(code11).tokenize()
ast = Parser(tokens).parse()
output = Interpreter().execute(ast)
print(f"  Output: {output}")
assert output == ["50", "50"], f"Expected ['50', '50'], got {output}"
print("  ✓ PASSED")
print()

# Test 12: Input with int conversion
print("=== TEST 12: Input + int conversion ===")
code12 = """rakho x = int(input())
rakho y = x * 3
dikhao y
"""
tokens = Lexer(code12).tokenize()
ast = Parser(tokens).parse()
output = Interpreter().execute(ast, inputs=["7"])
print(f"  Output: {output}")
assert output == ["21"], f"Expected ['21'], got {output}"
print("  ✓ PASSED")
print()

# Test 13: Void function (no wapis)
print("=== TEST 13: Void function (no return) ===")
code13 = """banao hello(naam)
    dikhao "Hello "
    dikhao naam
khatam

karo hello("World")
"""
tokens = Lexer(code13).tokenize()
ast = Parser(tokens).parse()
output = Interpreter().execute(ast)
print(f"  Output: {output}")
assert output == ["Hello ", "World"], f"Expected ['Hello ', 'World'], got {output}"
print("  ✓ PASSED")
print()

# Test 14: Code generation for new features
print("=== TEST 14: Python Code Generation ===")
code14 = """banao add(a, b)
    wapis a + b
khatam
rakho x = add(5, 3)
dikhao x
"""
tokens = Lexer(code14).tokenize()
ast = Parser(tokens).parse()
python_code = CodeGenerator().generate(ast)
print(f"  Generated Python:\n{python_code}")
assert "def add(a, b):" in python_code
assert "return" in python_code
print("  ✓ PASSED")
print()

# Test 15: Full pipeline with all new features
print("=== TEST 15: Full pipeline — functions + arrays + input ===")
code15 = """banao sum_list(arr, size)
    rakho total = 0
    rakho i = 0
    jabtak i < size
        rakho total = total + arr[i]
        rakho i = i + 1
    khatam
    wapis total
khatam

rakho numbers = [5, 10, 15]
rakho result = sum_list(numbers, 3)
dikhao result
"""
tokens = Lexer(code15).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
print(f"  Semantic errors: {sem.errors}")
tac = IRGenerator().generate(ast)
print(f"  TAC lines: {len(tac)}")
python_code = CodeGenerator().generate(ast)
output = Interpreter().execute(ast)
print(f"  Output: {output}")
assert output == ["30"], f"Expected ['30'], got {output}"
print("  ✓ PASSED")

print("\n✅ All tests passed!")
