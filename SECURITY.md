# 🛡 Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.x     | ✅ Yes    |
| 1.x     | ❌ No     |

---

## Reporting a Vulnerability

If you discover a security vulnerability in the Urdu Custom Compiler, please report it responsibly.

### How to Report

1. **Do NOT** open a public GitHub issue for security vulnerabilities.
2. Open a [private security advisory](../../security/advisories/new) on GitHub, or
3. Report via the project's [GitHub Issues](../../issues) with the `security` label (for non-critical issues).

### What to Include

- A clear description of the vulnerability.
- Steps to reproduce the issue.
- Potential impact assessment.
- Suggested fix (if any).

### Response Timeline

- **Acknowledgment:** Within 48 hours of receiving the report.
- **Investigation:** We will investigate and provide an initial assessment within 7 days.
- **Fix & Disclosure:** Once a fix is ready, we will coordinate disclosure with the reporter.

---

## Security Considerations

- This project is a **compiler/interpreter for a custom language**. User-submitted code is executed on the server via the `/run` endpoint.
- **Sandboxing:** The interpreter runs in the same process as the API server. Do **not** deploy this in a production environment without additional sandboxing (e.g., containers, restricted execution environments).
- **CORS:** The API allows all origins (`*`) by default for development. Restrict this in production.
- **Input Validation:** All code is parsed and validated through the compiler pipeline, but the interpreter has access to the host Python runtime. Treat all user input as untrusted.

---

## Known Limitations

- No code execution sandboxing — user code runs with the same privileges as the server process.
- No rate limiting on the `/run` endpoint.
- No authentication or authorization on API endpoints.

These are intentional for a development/educational tool. If you need to expose this publicly, implement appropriate safeguards.

---

Made with ❤ by H0NEYP0T-466
