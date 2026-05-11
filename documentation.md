# Mini Programming Language — Project Documentation

**A Roman Urdu Programming Language with Full Compiler Pipeline**

---

## Table of Contents

1. [Background of the Project](#background-of-the-project)
2. [Introduction](#introduction)
3. [Project Details](#project-details)
   - [Language Reference](#language-reference)
   - [Compiler Pipeline Architecture](#compiler-pipeline-architecture)
   - [Tech Stack](#tech-stack)
   - [Folder Structure](#folder-structure)
4. [Results / Output](#results--output)
5. [Conclusion](#conclusion)
6. [References](#references)

---

## Background of the Project

Programming languages like Python, Java, and C++ use English keywords (`if`, `while`, `print`, `return`) that create a barrier for non-English speakers. In Pakistan and other South Asian countries, millions of people communicate daily in Urdu but have limited English proficiency. This creates an unnecessary obstacle to learning programming.

The concept of **non-English programming languages** has existed since the 1980s — languages like Hindi Programming Language (HPLC), Bengali Programming Language (BASIC Bangla), and Arabic-based languages like جرب (Jarb) have explored this space. However, most of these efforts produced simple translators rather than full compiler implementations.

This project takes a different approach. Rather than building a thin wrapper around an existing language, we designed and implemented a **complete compiler pipeline** for a custom programming language with **Roman Urdu** (Urdu written in English letters) syntax. Roman Urdu was chosen because it is the most natural way Urdu speakers type on standard keyboards — it is how billions of Urdu messages are typed daily on WhatsApp, Facebook, and other platforms.

The result is a **Mini Programming Language** that supports variables, arithmetic, control flow (if/else, while loops), functions with recursion, arrays, user input, type casting, block scoping, and a full optimization pass — all written in Urdu keywords.

---

## Introduction

**Mini Programming Language** is a custom programming language with Roman Urdu syntax, paired with a complete compiler and interpreter implementation. The project consists of two main components:

1. **Backend** — A Python-based compiler that implements a full 7-stage pipeline: Lexical Analysis, Parsing, Semantic Analysis, Intermediate Representation (IR) Generation, Optimization, Python Code Generation, and Tree-Walk Interpretation. The backend is served through a FastAPI REST API.

2. **Frontend** — A React-based Web IDE featuring the Monaco Editor (the same editor that powers VS Code) with custom Urdu language syntax highlighting, real-time error marking, and tabbed visualization of every compiler stage.

A user writes code in Roman Urdu using keywords like `rakho` (declare), `dikhao` (print), `agar` (if), `warna` (else), `jabtak` (while), `banao` (function), `wapis` (return), and `karo` (call). When they press "Chalao" (Run), the code travels through all 7 pipeline stages, and the results — tokens, AST, semantic analysis, optimized TAC, generated Python, and program output — are displayed in real time.

### Key Design Principles

- **Zero external compiler tools** — No PLY, ANTLR, or other parser generators. Every stage is hand-written from scratch.
- **Educational focus** — Every pipeline stage is visible to the user. The IDE is designed to help students understand how compilers work.
- **Urdu-first error messages** — All error messages are written in Roman Urdu with helpful "did you mean?" suggestions for typos.
- **Block scoping** — Variables declared inside `agar` (if) and `jabtak` (while) blocks are local to that scope, teaching proper scoping concepts.

---

## Project Details

### Language Reference

#### Keywords

The language uses **16 keywords**, all written in Roman Urdu:

| Keyword | English Meaning | Usage |
|---------|----------------|-------|
| `rakho` | keep/put | Variable declaration/assignment: `rakho x = 10` |
| `dikhao` | show | Print to screen: `dikhao "hello"` |
| `agar` | if | Conditional: `agar x > 5 ... khatam` |
| `warna` | else | Else branch within agar block |
| `jabtak` | until/while | While loop: `jabtak x > 0 ... khatam` |
| `khatam | end/finished | Block terminator for agar, jabtak, and banao |
| `sahi` | correct/true | Boolean literal `true` |
| `ghalat` | wrong/false | Boolean literal `false` |
| `aur` | and | Logical AND operator |
| `ya` | or | Logical OR operator |
| `banao` | make/build | Function definition: `banao funcName(params) ... khatam` |
| `wapis` | return | Return from function: `wapis expr` |
| `karo` | do/make | Function call: `karo funcName(arg1, arg2)` |
| `input` | input | Read user input: `input("prompt")` |
| `int` | integer | Type cast to integer: `int(expr)` |
| `str` | string | Type cast to string: `str(expr)` |

#### Operators

| Operator | Meaning |
|----------|---------|
| `+` `-` `*` `/` | Arithmetic |
| `>` `<` `>=` `<=` `==` `!=` | Comparison |
| `!` | Logical NOT |
| `aur` | Logical AND |
| `ya` | Logical OR |
| `=` | Assignment |

#### Delimiters

| Symbol | Purpose |
|--------|---------|
| `( )` | Function parameters, function calls, grouping |
| `[ ]` | Array literals, array index access |
| `, | Separating function parameters, array elements |
| `#` | Single-line comment |

#### Data Types

- **Numbers** — Integers and floats: `42`, `3.14`
- **Strings** — Double-quoted: `"Assalam o Alaikum"`
- **Booleans** — `sahi` (true), `ghalat` (false)
- **Arrays** — Ordered lists: `[1, 2, 3]`, `["a", "b", "c"]`

#### Syntax Examples

**Variables and Printing:**
```
rakho naam = "Duniya"
rakho umar = 25
dikaho "Meri umar hai: "
dikhao umar
```

**Conditionals:**
```
rakho x = 10
agar x > 5
    dikhao "x bara hai"
warna
    dikhao "x chota hai ya barabar hai"
khatam
```

**While Loop:**
```
rakho x = 5
jabtak x > 0
    dikhao x
    rakho x = x - 1
khatam
dikhao "Khatam!"
```

**Functions:**
```
banao add(a, b)
    wapis a + b
khatam

banao greet(naam)
    dikhao "Assalam o Alaikum, "
    dikhao naam
khatam

karo greet("Fezan")
rakho result = add(10, 20)
dikhao result
```

**Arrays:**
```
rakho fruits = ["Aam", "Seb", "Kela"]
dikaho fruits[0]
rakho fruits[1] = "Anaar"
dikaho fruits[1]
```

**User Input:**
```
rakho naam = input("Apna naam likho: ")
dikaho "Salaam, " + naam
rakho x = int(input("Ek number likho: "))
rakho double = x * 2
dikaho double
```

**Logical Operators:**
```
rakho a = sahi
rakho b = ghalat
agar a aur b
    dikhao "Dono sahi hain"
warna
    dikhao "Koi ek ghalat hai"
khatam
```

---

### Compiler Pipeline Architecture

The compiler follows a classic multi-stage pipeline architecture. Each stage transforms the input from one representation to the next, with every stage's output visible in the Web IDE.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  LEXER   │───▶│  PARSER  │───▶│ SEMANTIC │───▶│    IR    │
│          │    │          │    │ ANALYZER │    │GENERATOR │
│ Tokenize │    │ Recursive│    │ Type chk │    │   TAC    │
│ source   │    │ descent  │    │ Scoping  │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                       │
                                                       ▼
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│INTERPRETER│◀──│  CODEGEN │◀──│OPTIMIZER │◀──│   TAC    │
│          │    │          │    │          │    │          │
│ Tree-walk│    │ Python   │    │ Constant │    │ Three    │
│ execute  │    │ output   │    │ folding  │    │ Address  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

#### Stage 1: Lexical Analysis (Lexer)

**File:** `backend/compiler/lexer.py`

The lexer converts raw source text into a flat stream of tokens. It is entirely hand-written with no external libraries.

- Recognizes **14 token types**: KEYWORD, IDENTIFIER, NUMBER, FLOAT, STRING, OPERATOR, ASSIGN, LPAREN, RPAREN, COMMA, LBRACKET, RBRACKET, NEWLINE, EOF
- Handles multi-character operators (`>=`, `<=`, `==`, `!=`) with look-ahead
- Skips whitespace and single-line `#` comments
- Produces Urdu error messages for malformed tokens (unterminated strings, unknown characters, invalid numbers)

#### Stage 2: Parsing (Parser)

**File:** `backend/compiler/parser.py`

A recursive-descent parser that builds an Abstract Syntax Tree (AST) from the token stream.

- Implements **operator precedence** (lowest to highest): `or (ya)` → `and (aur)` → `comparison` → `addition/subtraction` → `multiplication/division` → `unary` → `primary`
- Produces **18 AST node types** covering all language constructs
- Provides **"did you mean?" suggestions** using Levenshtein edit distance (≤2) for keyword typos
- Context-sensitive error messages — different guidance depending on what unexpected token was found
- Handles nested blocks with `khatam` terminator

#### Stage 3: Semantic Analysis

**File:** `backend/compiler/semantic.py`

Static analysis pass that validates the AST before execution.

- **Type checking** — Ensures operands are compatible (no string + int arithmetic)
- **Scope resolution** — Block scoping for `agar`/`jabtak`/`banao` blocks with parent scope chain
- **Undefined variable detection** — Catches use of variables before declaration
- **Static division by zero** — Detects `x / 0` at compile time
- **Function validation** — Checks function existence and argument count at call sites
- Returns a scoped symbol table with variable names, types, scope names, and depth

#### Stage 4: IR Generation (Three Address Code)

**File:** `backend/compiler/ir_generator.py`

Converts the AST into Three Address Code (TAC), a low-level intermediate representation.

- Uses temporary variables (`t0`, `t1`, `t2`...) and labels (`L0`, `L1`, `L2`...)
- Instruction forms: assignment, binary operation, print, label, conditional jump, goto, nop, return, function call, array operations
- Each TAC instruction has at most one operator and three operands (two sources, one destination)

#### Stage 5: Optimization

**File:** `backend/compiler/optimizer.py`

Applies three optimization passes to the TAC:

1. **Constant Propagation** — Replaces single-assignment variables with their literal values throughout the TAC
2. **Constant Folding** — Evaluates constant expressions at compile time (`t0 = 5 + 3` → `t0 = 8`)
3. **Dead Code Elimination** — Removes assignments to temporary variables that are never referenced

The folding pass runs twice to catch constants revealed by propagation.

#### Stage 6: Python Code Generation

**File:** `backend/compiler/codegen.py`

Translates the AST into valid, runnable Python source code.

- Maps Urdu keywords to Python: `aur` → `and`, `ya` → `or`, `sahi` → `True`, `ghalat` → `False`
- Proper indentation with 4-space blocks
- Generates Python `if/else`, `while`, `def`, `return`, `print()`, arrays, function calls, type casts, and `input()`

#### Stage 7: Interpretation

**File:** `backend/compiler/interpreter.py`

A tree-walk interpreter that executes the AST directly.

- **Environment-based scoping** — Each block creates a new `Environment` with a parent link for variable lookup
- **Function call stack** — Functions create new environments with bound parameters; returns use `ReturnSignal` for clean unwinding
- **Safety limits** — 10,000 iteration cap (infinite loop prevention), 100 call depth cap (infinite recursion prevention)
- **Input handling** — Accepts pre-supplied input strings for web API mode; falls back to Python `input()` in terminal mode

---

### Tech Stack

#### Backend

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.10+ |
| Web Framework | FastAPI | 0.115+ |
| ASGI Server | Uvicorn (standard) | 0.32+ |
| Validation | Pydantic | 2.0+ |

#### Frontend

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | TypeScript | 6.0+ |
| UI Framework | React | 19.2+ |
| Build Tool | Vite | 8.0+ |
| Code Editor | Monaco Editor (via @monaco-editor/react) | 4.7+ |

#### Architecture

- **Monorepo** — Single repository with `backend/` and `frontend/` directories
- **Communication** — REST API (`POST /run`) with JSON request/response
- **Ports** — Backend: 8008, Frontend: 5173
- **CORS** — Enabled for all origins (development mode)
- **No external compiler tools** — Entire compiler is hand-written in pure Python

---

### Folder Structure

```
Mini-Programming-Language/
├── backend/
│   ├── compiler/                    # Core compiler package
│   │   ├── __init__.py              # Package exports
│   │   ├── lexer.py                 # Tokenizer (Stage 1)
│   │   ├── parser.py                # Recursive-descent parser → AST (Stage 2)
│   │   ├── semantic.py              # Semantic analysis & type checking (Stage 3)
│   │   ├── ir_generator.py          # Three Address Code generation (Stage 4)
│   │   ├── optimizer.py             # Constant folding & propagation (Stage 5)
│   │   ├── codegen.py               # Python code generation (Stage 6)
│   │   ├── interpreter.py           # Tree-walk interpreter (Stage 7)
│   │   └── pretty_printer.py        # Terminal output formatting
│   ├── main.py                      # FastAPI application & /run endpoint
│   ├── test_pipeline.py             # Integration tests (15 test cases)
│   └── requirements.txt             # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── compiler.ts          # REST API client
│   │   ├── types/
│   │   │   └── compiler.ts          # TypeScript interfaces
│   │   ├── components/
│   │   │   ├── Editor.tsx           # Monaco code editor with Urdu syntax highlighting
│   │   │   ├── OutputPanel.tsx      # 6-tab results panel
│   │   │   ├── SemanticPanel.tsx    # Symbol table display
│   │   │   ├── TACPanel.tsx         # TAC before/after comparison
│   │   │   ├── PythonPanel.tsx      # Generated Python viewer
│   │   │   ├── ExamplesPanel.tsx    # 11 example programs sidebar
│   │   │   └── Toolbar.tsx          # Run / Clear / Toggle buttons
│   │   ├── App.tsx                  # Main application layout
│   │   └── main.tsx                 # React entry point
│   ├── visuals/                     # Screenshots & assets
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
└── README.md
```

---

## Results / Output

### The Web IDE

The project provides a fully functional web-based Integrated Development Environment (IDE) where users can write, run, and debug Urdu code while visualizing every compiler stage.

**Web IDE Overview:**

![Web IDE Screenshot](frontend/visuals/WEB%20UI.PNG)

*The complete Web IDE with Monaco Editor, sidebar examples, and tabbed output panels*

### Stage 1: Lexer Output

The lexer converts source code into a stream of classified tokens:

![Lexer Token Stream](frontend/visuals/tokens.PNG)

*Token stream showing each word, operator, and literal classified with position info*

![Lexer Web UI Panel](frontend/visuals/server_imgof_LEXER.PNG)

*Web IDE — Lexer panel showing the full token list with type, value, and line number*

### Stage 2: Parser Output (AST)

The parser builds a hierarchical Abstract Syntax Tree from the token stream:

![Parser AST](frontend/visuals/ast.PNG)

*AST: hierarchical tree showing the program's syntactic structure*

![Parser AST and Symbol Table](frontend/visuals/server_img_parser_symboltable.PNG)

*Web IDE — Parser panel with AST tree*

### Stage 3: Semantic Analysis Output

The semantic analyzer validates types, scopes, and variable declarations:

![Semantic Analysis](frontend/visuals/semantic.PNG)

*Semantic output: symbol table with types, scopes, errors, and warnings*

### Stage 4 & 5: TAC and Optimization

The IR generator produces Three Address Code, which the optimizer then improves:

![TAC](frontend/visuals/tac.PNG)

*TAC instructions: original (unoptimized) vs. optimized after constant folding*

![TAC Optimization and Python](frontend/visuals/server_imgof_tac_optimization_pythoncde_output.PNG)

*Web IDE — TAC, optimization diff, and generated Python all visible*

### Stage 6: Python Code Generation

The code generator transpiles Urdu code into equivalent Python:

![Generated Python](frontend/visuals/python_code.PNG)

*Generated Python: the Urdu program translated to executable Python*

### Stage 7: Program Execution

The tree-walk interpreter executes the AST and produces the final output:

![Execution with Output](frontend/visuals/execution_with_output.PNG)

*Web IDE — Final output panel showing the result of program execution*

### Example Programs

The IDE includes **11 built-in example programs** demonstrating every language feature:

| # | Example | Features Demonstrated |
|---|---------|----------------------|
| 1 | Hello World | Basic printing |
| 2 | If / Else | Conditional branching with `agar`/`warna` |
| 3 | While Loop Counter | Loops with `jabtak`/`khatam` |
| 4 | Arithmetic | All arithmetic operators |
| 5 | Constant Folding | Compile-time constant evaluation |
| 6 | Constant Propagation | Variable-to-constant substitution |
| 7 | Boolean Logic | `aur`, `ya`, `sahi`, `ghalat` |
| 8 | Semantic Error | Error detection demonstration |
| 9 | Functions | `banao`, `wapis`, `karo` — function definition, return, call |
| 10 | Arrays | Array creation, access, and index assignment |
| 11 | User Input | `input()`, `int()`, `str()` — type casting with input |

### API Response Example

When code is submitted via `POST /run`, the API returns a comprehensive JSON response:

```json
{
  "output": "42",
  "tokens": [
    { "index": 0, "type": "KEYWORD", "value": "rakho", "line": 1 },
    { "index": 1, "type": "IDENTIFIER", "value": "x", "line": 1 },
    { "index": 2, "type": "ASSIGN", "value": "=", "line": 1 },
    { "index": 3, "type": "NUMBER", "value": "42", "line": 1 }
  ],
  "ast": "ASSIGN x =\n  NUM 42",
  "semantic": {
    "errors": [],
    "warnings": [],
    "symbol_table": { "x": "int" },
    "scoped_symbols": [
      { "name": "x", "var_type": "int", "scope": "global", "scope_depth": 0 }
    ]
  },
  "tac": {
    "original": ["x = 42"],
    "optimized": ["x = 42"],
    "changes": ["No optimizations applicable"]
  },
  "generated_python": "x = 42\nprint(x)"
}
```

---

## Conclusion

This project demonstrates the complete design and implementation of a **Mini Programming Language** with Roman Urdu syntax. From the ground up, we built:

1. **A custom programming language** with 16 Urdu keywords supporting variables, arithmetic, control flow (if/else, while), functions with recursion, arrays, user input, type casting, and block scoping.

2. **A full 7-stage compiler pipeline** — entirely hand-written in Python with zero external compiler tools — that transforms Urdu source code through lexing, parsing, semantic analysis, IR generation, optimization, Python code generation, and interpretation.

3. **A modern Web IDE** built with React and Monaco Editor that provides real-time visualization of every compiler stage, making it an effective educational tool for understanding how compilers work.

The project proves that programming languages do not have to be English-centric. By using Roman Urdu syntax — the natural way Urdu speakers type on standard keyboards — we lower the barrier to programming education for millions of Urdu speakers. The complete pipeline implementation (rather than a thin wrapper) ensures that the language is a genuine programming language with proper scoping, type checking, optimization, and code generation.

### Future Enhancements

- **File I/O operations** — Reading and writing files from within the language
- **String manipulation functions** — Built-in string operations like `length`, `upper`, `lower`, `split`
- **Nested arrays / 2D arrays** — Multi-dimensional array support
- **Error handling** — Try/catch-style exception handling with `koshish`/`khata` keywords
- **Module system** — Importing and organizing code across multiple files
- **More optimization passes** — Loop unrolling, strength reduction, common subexpression elimination
- **Standalone interpreter** — Running `.urdu` files from the command line without the web IDE

---

## References

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd Edition). Pearson Education. — The standard textbook on compiler design covering all pipeline stages implemented in this project.

2. FastAPI Documentation. (2024). *FastAPI Framework*. https://fastapi.tiangolo.com/ — The web framework used for the backend API.

3. Microsoft Monaco Editor. (2024). *Monaco Editor*. https://microsoft.github.io/monaco-editor/ — The code editor component powering the web IDE.

4. React Documentation. (2024). *React Library*. https://react.dev/ — The frontend UI framework.

5. Pydantic Documentation. (2024). *Pydantic Validation*. https://docs.pydantic.dev/ — Data validation for API request/response models.

6. Python Dataclasses. (2024). *Python Standard Library*. https://docs.python.org/3/library/dataclasses.html — Used for AST node definitions.

7. Levenshtein Distance Algorithm. (n.d.). *Edit Distance*. https://en.wikipedia.org/wiki/Levenshtein_distance — Used for "did you mean?" typo suggestions in the parser.

---

*Project developed as a semester project demonstrating compiler design and implementation concepts.*
