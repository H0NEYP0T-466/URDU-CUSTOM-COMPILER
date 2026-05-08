# 🤝 Contributing to Urdu Custom Compiler

Thank you for your interest in contributing! This document outlines how to participate in the project.

---

## 🚀 Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/URDU-CUSTOM-COMPILER.git
   cd URDU-CUSTOM-COMPILER
   ```
3. **Set up the backend:**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```
4. **Set up the frontend:**
   ```bash
   cd frontend
   npm install
   ```
5. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feat/my-new-feature
   # or
   git checkout -b fix/issue-description
   ```

---

## 📝 Code Style & Linting

### Python (Backend)
- Follow **PEP 8** conventions.
- Use **type annotations** on all function signatures.
- Format with **black** and lint with **ruff**:
  ```bash
  black .
  ruff check .
  ```
- Run type checking:
  ```bash
  mypy backend/
  ```

### TypeScript / React (Frontend)
- Follow the existing component structure (one component per file with co-located CSS).
- Use **strict** TypeScript — no `any` types.
- Format with **Prettier**:
  ```bash
  npx prettier --write "frontend/src/**/*.{ts,tsx,css}"
  ```
- Run the TypeScript compiler:
  ```bash
  npx tsc --noEmit
  ```

---

## 🧪 Testing

- Backend tests: `pytest backend/ --cov=backend`
- Frontend type check: `npx tsc --noEmit`
- Run the full pipeline test: `python backend/test_pipeline.py`
- Ensure all existing tests pass before submitting a PR.

---

## 🐛 Bug Reports

If you find a bug, please [open an issue](../../issues/new?template=bug_report.yml) with:

- A clear, descriptive title.
- Steps to reproduce the problem.
- Expected vs. actual behavior.
- Your environment (OS, Python version, Node version).
- Relevant logs or error messages.
- Screenshots if applicable.

---

## ✨ Feature Requests

To propose a new feature, [open an issue](../../issues/new?template=feature_request.yml) with:

- The problem you're trying to solve.
- Your proposed solution.
- Any alternative approaches you've considered.
- Potential risks or scope boundaries.

---

## 🔀 Pull Request Process

1. Ensure your code follows the style guidelines above.
2. Add or update tests for any changed functionality.
3. Update documentation (README, docstrings, comments) as needed.
4. Verify the build passes:
   - Backend: `uvicorn main:app --reload --port 8008` runs without errors.
   - Frontend: `npm run build` completes successfully.
5. Fill out the PR template completely.
6. Link any related issues (e.g., `Fixes #123`).
7. Request review from a maintainer.

---

## 📚 Documentation Updates

When changing functionality, please update:

- **README.md** — if adding features, changing setup, or modifying the API.
- **Code comments** — for non-obvious logic.
- **Type annotations** — always keep them current.
- **Example programs** — if the language syntax changes.

---

## 💬 Communication

- Use **GitHub Issues** for bug reports and feature requests.
- Use **GitHub Discussions** for questions, ideas, and general conversation.
- Be respectful and constructive in all interactions.

---

## 📜 Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

Made with ❤ by the Urdu Custom Compiler community
