# 🐛 Bug-Bounty-Cal-Report

**Bug bounty CVSS calculator + report generator with a FastAPI server.** 🎯
Score any finding with a real CVSS v3.1 engine, then turn it into a clean,
submission-ready markdown report — from Python or over HTTP.

---

## ✨ Features

- 🧮 **Real CVSS v3.1 scoring** — official FIRST.org equations, including the spec roundup (no approximations)
- 🔤 **Vector string or metric kwargs** — paste a full `CVSS:3.1/...` vector, or pass metrics one by one
- 🏷️ **Severity bands built in** — None / Low / Medium / High / Critical, mapped from the score
- 🌐 **FastAPI server** — health check, `/calculate`, and `/report` endpoints out of the box
- 📝 **Instant report drafts** — title, target, severity, vector, description, impact, remediation in markdown
- 🧪 **13 verified tests** — engine scores checked against FIRST.org reference values
- 📦 **Pure stdlib calculator** — the scoring engine has zero dependencies
- 🐳 **Docker-compatible** — Dockerfile + compose included for local use (not published to any registry)

---

## 🧮 The CVSS Engine

`src/modules/cvss_calculator.py` parses a CVSS:3.1 (or 3.0) vector, applies
the official base-score equations — Impact from C/I/A, Exploitability from
AV × AC × PR × UI, with Privileges Required weighted by Scope — and rounds
with the CVSS spec roundup.

### 📊 Severity bands

| Score | Severity |
|---|---|
| 0.0 | ⚪ None |
| 0.1 – 3.9 | 🟢 Low |
| 4.0 – 6.9 | 🟡 Medium |
| 7.0 – 8.9 | 🟠 High |
| 9.0 – 10.0 | 🔴 Critical |

### ✅ Reference scores (verified in the test suite)

| Vector | Score | Severity |
|---|---|---|
| `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | 9.8 | 🔴 Critical |
| `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` | 10.0 | 🔴 Critical |
| `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` | 7.5 | 🟠 High |
| `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N` | 6.1 | 🟡 Medium |
| `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N` | 0.0 | ⚪ None |

---

## 🐍 Python Usage

```python
from src.modules.cvss_calculator import calculate_cvss

# Full vector string
result = calculate_cvss("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
print(result["base_score"])  # 9.8
print(result["severity"])    # Critical

# Or metric by metric — same result
result = calculate_cvss(av="N", ac="L", pr="N", ui="N", s="U", c="H", i="H", a="H")
```

Invalid vectors and missing metrics raise `ValueError` with a clear message. ⚠️

---

## 🌐 API Server

```bash
uvicorn src.api_server:app --host 0.0.0.0 --port 8000
```

| Method | Endpoint | What it does |
|---|---|---|
| `GET` | `/` | ❤️ Health check |
| `POST` | `/calculate` | 🧮 Score a CVSS vector |
| `POST` | `/report` | 📝 Build a scored markdown report |

### 🧮 Calculate

```bash
curl -X POST http://127.0.0.1:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}'
```

```json
{"base_score": 9.8, "severity": "Critical", "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", "version": "3.1"}
```

### 📝 Report

```bash
curl -X POST http://127.0.0.1:8000/report \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Reflected XSS in search",
    "target": "https://example.com/search",
    "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
    "description": "Query parameter is reflected unsanitised."
  }'
```

Returns the score, severity, and a ready-to-file markdown report. 🚀
Bad vectors get a clean `400` with the reason — never a stack trace.

---

## 🚀 Quickstart

```bash
# Install (with dev tools for the tests)
pip install -e ".[dev]"

# Run the API
uvicorn src.api_server:app --host 0.0.0.0 --port 8000

# Run the tests
pytest tests/ -v
```

**Requirements:** Python 3.11+ 🐍

---

## 🧪 Tests

**13 tests, all passing.** ✅

- 🎯 **Engine tests** (`tests/test_engine.py`) — the five FIRST.org reference scores above, kwargs/vector equivalence, severity bands, and error handling for invalid or incomplete vectors
- 🌐 **API tests** (`tests/test_api.py`) — health, calculate, invalid-vector `400`, and the full report flow through the FastAPI TestClient

---

## 🔄 CI

GitHub Actions (`.github/workflows/test.yml`) runs on every push and pull request:

1. 📥 Checkout
2. 🐍 Set up Python 3.11
3. 📦 `pip install -e ".[dev]"`
4. 🧪 `pytest tests/ -v`

---

## 🐳 Docker (optional, local only)

Docker-compatible, for local use — this project is **not published** to Docker Hub or any registry. 🏠

```bash
docker build -t bug-bounty-cal-report .
docker run -p 8000:8000 bug-bounty-cal-report
```

or with compose:

```bash
docker compose up
```

The image runs as a non-root user with a built-in health check on `/`. ❤️

---

## 📁 Project Structure

    📁 Bug-Bounty-Cal-Report/
    ├── 📄 README.md
    ├── 📄 pyproject.toml
    ├── 📄 conftest.py
    ├── 🐳 Dockerfile
    ├── 📄 .dockerignore
    ├── 🐳 docker-compose.yml
    ├── 📁 .github/workflows/
    │   └── 📄 test.yml
    ├── 📁 src/
    │   ├── 📄 __init__.py
    │   ├── 🌐 api_server.py
    │   └── 📁 modules/
    │       ├── 📄 __init__.py
    │       └── 🧮 cvss_calculator.py
    └── 📁 tests/
        ├── 🧪 test_api.py
        └── 🧪 test_engine.py

---

## 🎯 What it's for

Bug bounty work runs on triage speed: paste a vector, get an exact score and
severity, generate the report skeleton, and spend your time on the finding
itself — not on score math. 🔥
