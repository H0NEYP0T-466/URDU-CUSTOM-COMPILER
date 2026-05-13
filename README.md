# URDU-CUSTOM-COMPILER 🇵🇰

<p align="center">

  <!-- Core -->
  ![GitHub License](https://img.shields.io/github/license/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=brightgreen)
  ![GitHub Stars](https://img.shields.io/github/stars/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=yellow)
  ![GitHub Forks](https://img.shields.io/github/forks/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=blue)
  ![GitHub Issues](https://img.shields.io/github/issues/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=red)
  ![GitHub Pull Requests](https://img.shields.io/github/issues-pr/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=orange)
  ![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge)

  <!-- Activity -->
  ![Last Commit](https://img.shields.io/github/last-commit/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=purple)
  ![Commit Activity](https://img.shields.io/github/commit-activity/m/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=teal)
  ![Repo Size](https://img.shields.io/github/repo-size/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=blueviolet)
  ![Code Size](https://img.shields.io/github/languages/code-size/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=indigo)

  <!-- Languages -->
  ![Top Language](https://img.shields.io/github/languages/top/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=critical)
  ![Languages Count](https://img.shields.io/github/languages/count/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=success)

  <!-- Community -->
  ![Discussions](https://img.shields.io/github/discussions/H0NEYP0T-466/URDU-CUSTOM-COMPILER?style=for-the-badge&color=blue)
  ![Documentation](https://img.shields.io/badge/Docs-Available-green?style=for-the-badge&logo=readthedocs&logoColor=white)
  ![Open Source Love](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red?style=for-the-badge)

</p>

<p align="center">
  <img src="frontend/visuals/WEB UI.PNG" alt="Urdu Custom Compiler — Web IDE Screenshot" width="900" />
</p>

<p align="center"><em>🖥 The Web IDE — Monaco Editor with real-time compiler pipeline visualization</em></p>

**ایک کسٹم زبان** — A custom programming language compiler and interpreter with **Roman Urdu** syntax. Write code in Urdu using familiar keywords, and watch it compile through a full pipeline: Lexer → Parser → Semantic Analysis → IR Generation → Optimization → Code Generation → Interpretation.

---

## 🔗 Quick Links

| | |
|---|---|
| 🌐 **Live Demo** | Run locally (see [Installation](#-installation)) |
| 📖 **Docs** | This README + inline code docs |
| 🐛 **Issues** | [GitHub Issues](https://github.com/H0NEYP0T-466/URDU-CUSTOM-COMPILER/issues) |
| 🤝 **Contributing** | [CONTRIBUTING.md](CONTRIBUTING.md) |

---

## 📑 Table of Contents

- [Features](#-features)
- [Language Reference](#-language-reference)
- [Quick Start](#-installation)
- [Usage Examples](#-usage-examples)
- [Architecture](#-architecture)
- [Compiler Pipeline Visualizations](#-compiler-pipeline-visualizations)
- [Folder Structure](#-folder-structure)
- [Tech Stack](#-tech-stack)
- [Dependencies & Packages](#-dependencies--packages)
- [Contributing](#-contributing)
- [License](#-license)
- [Security](#-security)
- [Code of Conduct](#-code-of-conduct)

---

## ✨ Features

- 🇵🇰 **Roman Urdu Syntax** — Write code using 12 Urdu keywords (`rakho`, `dikhao`, `agar`, `warna`, `jabtak`, `functionbnao`, `wapisbejo`, and more)
- 🔬 **Full Compiler Pipeline** — Lexer → Parser → Semantic Analysis → TAC IR → Optimizer → Python Codegen → Interpreter
- 🎨 **Web IDE** — Monaco Editor (the same editor as VS Code) with custom syntax highlighting, error markers, and a dark theme
- 📊 **Compiler Visualization** — View tokens, AST, TAC (Three Address Code), optimized IR, generated Python, and semantic symbol tables in real time
- ⚡ **Three Optimization Passes** — Constant propagation, constant folding, and dead code elimination at the IR level
- 🔒 **Semantic Analysis** — Type checking, scope resolution, undeclared variable detection, division-by-zero detection
- 📦 **Block Scoping** — Variables declared inside `agar`/`jabtak`/`functionbnao` blocks are local to that scope
- 🐍 **Python Code Generation** — Transpiles Urdu code to equivalent, runnable Python
- 🌐 **REST API** — FastAPI backend with a single `POST /run` endpoint
- 📱 **Responsive Split-Pane UI** — Resizable editor and output panels
- 🔧 **Function Definitions** — Define reusable functions with `functionbnao`, parameters, and `wapisbejo` return
- 📋 **Arrays** — Create arrays with `[1, 2, 3]`, access by index `arr[0]`, and modify elements `arr[0] = 99`
- 📝 **11 Built-in Examples** — Sidebar with runnable examples: Hello World, If/Else, While, Arithmetic, Functions, Arrays, and more
- 🧪 **Integration Tests** — 12 test cases covering the full pipeline including functions, arrays, scoping, and optimization

---

## 🇵🇰 Language Reference

### Keywords

| Keyword        | Meaning                |
|----------------|------------------------|
| `rakho`        | Declare/assign a variable |
| `dikhao`       | Print to output        |
| `agar`         | If statement           |
| `warna`        | Else clause            |
| `jabtak`       | While loop             |
| `khatam`       | End a block            |
| `sahi`         | Boolean true           |
| `ghalat`       | Boolean false          |
| `aur`          | Logical AND            |
| `ya`           | Logical OR             |
| `functionbnao` | Define a function      |
| `wapisbejo`    | Return from function   |

### Operators

| Operator | Meaning          |
|----------|------------------|
| `+ - * /` | Arithmetic     |
| `> < >= <= == !=` | Comparison |
| `!`      | Logical NOT      |
| `aur`    | Logical AND      |
| `ya`     | Logical OR       |

### Data Types

- **Numbers** — Integers and floats: `42`, `3.14`
- **Strings** — Double-quoted: `"Assalam o Alaikum"`
- **Booleans** — `sahi` (true), `ghalat` (false)
- **Arrays** — Ordered lists: `[10, 20, 30]`, accessible by index `arr[0]`

---

## 🚀 Installation

### Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
uvicorn main:app --reload --port 8008
```

The API will be available at `http://localhost:8008`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## ⚡ Usage Examples

### Example 1: Hello World

```
rakho naam = "Duniya"
dikaho "Assalam o Alaikum, "
dikaho naam
```

**Output:**
```
Assalam o Alaikum,
Duniya
```

### Example 2: If/Else

```
rakho x = 10
agar x > 5
    dikhao "x bara hai"
warna
    dikhao "x chota hai"
khatam
```

**Output:**
```
x bara hai
```

### Example 3: While Loop

```
rakho x = 3
jabtak x > 0
    dikhao x
    rakho x = x - 1
khatam
```

**Output:**
```
3
2
1
```

### Example 4: Block Scoping

```
rakho x = 10
agar x > 5
    rakho inner = 99
    dikhao inner
khatam
dikhao x
```

**Output:**
```
99
10
```

### Example 5: Logical Operators

```
rakho a = sahi
rakho b = ghalat
agar a aur b
    dikhao "dono sahi hain"
warna
    dikhao "koi ek ghalat hai"
khatam
```

**Output:**
```
koi ek ghalat hai
```

### Example 6: Functions — Definition & Return

```
functionbnao add(a, b)
    wapisbejo a + b
khatam

rakho result = add(3, 4)
dikaho result
```

**Output:**
```
7
```

### Example 7: Functions — Call in Expression

```
functionbnao double(x)
    wapisbejo x * 2
khatam

dikaho double(5) + 3
```

**Output:**
```
13
```

### Example 8: Arrays — Creation & Access

```
rakho nums = [10, 20, 30]
dikaho nums[0]
dikaho nums[2]
```

**Output:**
```
10
30
```

### Example 9: Arrays — Index Assignment

```
rakho nums = [10, 20, 30]
rakho nums[1] = 99
dikaho nums[1]
```

**Output:**
```
99
```

### Example 10: Functions + Arrays + While Loop

```
functionbnao sum_list(arr, size)
    rakho total = 0
    rakho i = 0
    jabtak i < size
        rakho total = total + arr[i]
        rakho i = i + 1
    khatam
    wapisbejo total
khatam

rakho mylist = [1, 2, 3, 4, 5]
dikaho sum_list(mylist, 5)
```

**Output:**
```
15
```

### API Usage (cURL)

```bash
curl -X POST http://localhost:8008/run \
  -H "Content-Type: application/json" \
  -d '{"code": "rakho x = 42\ndikhao x"}'
```

**Response:**
```json
{
  "output": "42",
  "tokens": [...],
  "ast": "ASSIGN x =\n  NUM 42\nPRINT\n  VAR x",
  "semantic": { "errors": [], "warnings": [], "symbol_table": {...} },
  "tac": { "original": [...], "optimized": [...], "changes": [...] },
  "generated_python": "x = 42\nprint(x)"
}
```

---

## 🏗 Architecture

The compiler follows a classic multi-stage pipeline:

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
│ execute  │    │ output   │    │ prop/fold│    │ Address  │
│          │    │          │    │ + DCE    │    │ Code     │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### Pipeline Stages

1. **Lexer** (`compiler/lexer.py`) — Converts source text into tokens. Handles keywords, operators, literals, and comments.
2. **Parser** (`compiler/parser.py`) — Recursive-descent parser that builds an Abstract Syntax Tree (AST).
3. **Semantic Analyzer** (`compiler/semantic.py`) — Type checking, scope resolution, undeclared variable detection, scoped symbol table.
4. **IR Generator** (`compiler/ir_generator.py`) — Converts AST to Three Address Code (TAC).
5. **Optimizer** (`compiler/optimizer.py`) — Three optimization passes on TAC: constant propagation, constant folding, and dead code elimination.
6. **Code Generator** (`compiler/codegen.py`) — Translates AST to equivalent Python source code.
7. **Interpreter** (`compiler/interpreter.py`) — Tree-walk interpreter that executes the AST directly.

---

## 📸 Compiler Pipeline Visualizations

See the compiler in action — every stage of the pipeline visualized in the Web UI.

### Stage 1: Lexer — Tokenization

The Lexer converts raw Urdu source code into a stream of tokens, each tagged with type, value, line, and column.

<p align="center">
  <img src="frontend/visuals/tokens.PNG" alt="Lexer — Token stream output" width="700" />
</p>

<p align="center"><em>Token stream: each word, operator, and literal classified with position info</em></p>

<p align="center">
  <img src="frontend/visuals/server_imgof_LEXER.PNG" alt="Lexer — Web UI token panel" width="900" />
</p>

<p align="center"><em>Web IDE — Lexer panel showing the full token list</em></p>

### Stage 2: Parser — Abstract Syntax Tree (AST)

The Parser consumes the token stream and builds a tree representation of the program structure using recursive descent.

<p align="center">
  <img src="frontend/visuals/ast.PNG" alt="Parser — Abstract Syntax Tree" width="700" />
</p>

<p align="center"><em>AST: hierarchical tree showing the program's syntactic structure</em></p>

<p align="center">
  <img src="frontend/visuals/server_img_parser_symboltable.PNG" alt="Parser — AST and Symbol Table in Web UI" width="900" />
</p>

<p align="center"><em>Web IDE — Parser panel with AST tree and symbol table</em></p>

### Stage 3: Semantic Analysis — Type Checking & Scoping

The Semantic Analyzer validates the AST: type checking, scope resolution, undeclared variable detection, and scoped symbol table construction.

<p align="center">
  <img src="frontend/visuals/semantic.PNG" alt="Semantic Analyzer — Symbol table, errors, and warnings" width="700" />
</p>

<p align="center"><em>Semantic output: symbol table with types, scopes, errors, and warnings</em></p>

### Stage 4: TAC — Three Address Code Generation

The IR Generator converts the AST into Three Address Code (TAC), a low-level intermediate representation.

<p align="center">
  <img src="frontend/visuals/tac.PNG" alt="TAC — Three Address Code (original and optimized)" width="700" />
</p>

<p align="center"><em>TAC instructions: original (unoptimized) vs. optimized after constant propagation, constant folding, and dead code elimination</em></p>

### Stage 5: Optimization — Constant Propagation, Folding & Dead Code Elimination

The Optimizer runs three passes on the TAC instructions: **constant propagation** (substitutes single-assignment variables with their literal values), **constant folding** (evaluates constant expressions like `3 + 4` to `7` at compile time), and **dead code elimination** (removes unused temporary variable assignments).

<p align="center">
  <img src="frontend/visuals/server_imgof_tac_optimization_pythoncde_output.PNG" alt="TAC, Optimization, and Python Code — Full pipeline view" width="900" />
</p>

<p align="center"><em>Web IDE — TAC, optimization diff, and generated Python all visible</em></p>

### Stage 6: Code Generation — Python Output

The Code Generator translates the AST into equivalent Python source code.

<p align="center">
  <img src="frontend/visuals/python_code.PNG" alt="Code Generator — Generated Python code" width="700" />
</p>

<p align="center"><em>Generated Python: the Urdu program translated to executable Python</em></p>

### Stage 7: Execution — Interpreter Output

The tree-walk interpreter executes the AST directly and produces the final program output.

<p align="center">
  <img src="frontend/visuals/execution_with_output.PNG" alt="Interpreter — Program execution with output" width="900" />
</p>

<p align="center"><em>Web IDE — Final output panel showing the result of program execution</em></p>

---

## 📂 Folder Structure

```
URDU-CUSTOM-COMPILER/
├── backend/
│   ├── compiler/              # Core compiler package
│   │   ├── __init__.py        # Package exports
│   │   ├── lexer.py           # Tokenizer
│   │   ├── parser.py          # Recursive-descent parser → AST
│   │   ├── semantic.py        # Semantic analysis & type checking
│   │   ├── ir_generator.py    # Three Address Code generation
│   │   ├── optimizer.py       # Constant folding optimization
│   │   ├── codegen.py         # Python code generation
│   │   ├── interpreter.py     # Tree-walk interpreter
│   │   └── pretty_printer.py  # Terminal output formatting
│   ├── main.py                # FastAPI application & /run endpoint
│   ├── test_pipeline.py       # Integration tests
│   ├── requirements.txt       # Python dependencies
│   └── run_commands.txt       # Quick start commands
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── compiler.ts    # REST API client
│   │   ├── components/
│   │   │   ├── Editor.tsx     # Monaco code editor
│   │   │   ├── Editor.css
│   │   │   ├── OutputPanel.tsx    # Execution output display
│   │   │   ├── OutputPanel.css
│   │   │   ├── TACPanel.tsx       # TAC visualization
│   │   │   ├── TACPanel.css
│   │   │   ├── SemanticPanel.tsx  # Symbol table display
│   │   │   ├── SemanticPanel.css
│   │   │   ├── PythonPanel.tsx    # Generated Python view
│   │   │   ├── PythonPanel.css
│   │   │   ├── ExamplesPanel.tsx  # Example programs sidebar
│   │   │   ├── ExamplesPanel.css
│   │   │   ├── Toolbar.tsx        # Run / Clear / Toggle buttons
│   │   │   └── Toolbar.css
│   │   ├── types/
│   │   │   └── compiler.ts    # TypeScript interfaces
│   │   ├── App.tsx            # Main application layout
│   │   ├── App.css
│   │   ├── main.tsx           # React entry point
│   │   └── index.css          # Global design tokens
│   ├── visuals/               # Screenshots & assets
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   └── config.yml
│   └── pull_request_template.md
│
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
└── README.md
```

---

## 🛠 Tech Stack

### Languages
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)

### Frameworks & Libraries
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Monaco Editor](https://img.shields.io/badge/Monaco_Editor-68217A?style=for-the-badge&logo=visualstudiocode&logoColor=white)

### DevOps / CI / Tools
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![npm](https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---

## 📦 Dependencies & Packages

### Runtime Dependencies

<details>
<summary><strong>🐍 Python (Backend)</strong></summary>

| Package | Version | Description |
|---------|---------|-------------|
| ![FastAPI](https://img.shields.io/pypi/v/fastapi?style=for-the-badge&label=fastapi) | v0.115+ | High-performance async web framework |
| ![Uvicorn](https://img.shields.io/pypi/v/uvicorn?style=for-the-badge&label=uvicorn) | v0.34+ | ASGI server for running FastAPI |
| ![Pydantic](https://img.shields.io/pypi/v/pydantic?style=for-the-badge&label=pydantic) | v2.10+ | Data validation using Python type annotations |

</details>

<details>
<summary><strong>⚛️ Node.js (Frontend)</strong></summary>

| Package | Version | Description |
|---------|---------|-------------|
| ![React](https://img.shields.io/npm/v/react?style=for-the-badge&label=react) | v19.2.5 | UI component library |
| ![React DOM](https://img.shields.io/npm/v/react-dom?style=for-the-badge&label=react--dom) | v19.2.5 | React rendering for the DOM |
| ![Monaco Editor](https://img.shields.io/npm/v/@monaco-editor/react?style=for-the-badge&label=@monaco-editor%2Freact) | v4.7.0 | VS Code's code editor as a React component |

</details>

### Dev / Build / Test Dependencies

<details>
<summary><strong>⚛️ Node.js (Frontend)</strong></summary>

| Package | Version | Description |
|---------|---------|-------------|
| ![TypeScript](https://img.shields.io/npm/v/typescript?style=for-the-badge&label=typescript) | v6.0.2 | Typed superset of JavaScript |
| ![Vite](https://img.shields.io/npm/v/vite?style=for-the-badge&label=vite) | v8.0.10 | Next-gen frontend build tool |
| ![Vite Plugin React](https://img.shields.io/npm/v/@vitejs/plugin-react?style=for-the-badge&label=@vitejs%2Fplugin--react) | v6.0.1 | Fast Refresh for Vite + React |
| ![@types/react](https://img.shields.io/npm/v/@types/react?style=for-the-badge&label=@types%2Freact) | v19.2.14 | TypeScript types for React |
| ![@types/react-dom](https://img.shields.io/npm/v/@types/react-dom?style=for-the-badge&label=@types%2Freact--dom) | v19.2.3 | TypeScript types for React DOM |

</details>

---

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to get started, code style guidelines, and the PR process.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🛡 Security

See our [Security Policy](SECURITY.md) for information on reporting vulnerabilities and known security considerations.

---

## 📏 Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

<p align="center">Made with ❤ by <a href="https://github.com/H0NEYP0T-466">H0NEYP0T-466</a></p>
