# URDU-CUSTOM-COMPILER 🇵🇰

**ایک کسٹم زبان** — A custom programming language interpreter with Roman Urdu syntax.

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | React 19 + TypeScript + Monaco Editor |
| Backend   | FastAPI (Python 3.10+)              |
| Compiler  | Hand-written Lexer → Parser → Interpreter |
| Styling   | Vanilla CSS (per-component files)   |

## Language Keywords

| Keyword  | Meaning          |
|----------|------------------|
| rakho    | declare/assign   |
| dikhao   | print            |
| agar     | if               |
| warna    | else             |
| jabtak   | while loop       |
| khatam   | end block        |
| sahi     | true             |
| ghalat   | false            |
| aur      | and              |
| ya       | or               |

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8008
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## Example Program
```
rakho x = 10
agar x > 5
    dikhao "x bara hai"
warna
    dikhao "x chota hai"
khatam
```

## Architecture

```
backend/
├── compiler/
│   ├── lexer.py        # Tokenizer
│   ├── parser.py       # Recursive-descent parser → AST
│   └── interpreter.py  # Tree-walk interpreter
└── main.py             # FastAPI endpoint

frontend/
├── src/
│   ├── components/     # Editor, OutputPanel, Toolbar, ExamplesPanel
│   ├── api/            # REST client
│   ├── App.tsx         # Main layout
│   └── index.css       # Design tokens
└── package.json
```
