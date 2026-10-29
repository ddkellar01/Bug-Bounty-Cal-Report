"""Bug Bounty Cal-Report API server (FastAPI).

Endpoints:
    GET  /          health check
    POST /calculate {"vector": "CVSS:3.1/..."} -> base score + severity
    POST /report    finding details -> scored markdown bug bounty report
"""

from src.modules.cvss_calculator import calculate_cvss

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Bug Bounty Cal-Report", version="1.0.0")


class CalculateRequest(BaseModel):
    vector: str


class ReportRequest(BaseModel):
    title: str
    target: str
    vector: str
    description: str = ""
    impact: str = ""
    remediation: str = ""


@app.get("/")
def health() -> dict:
    return {"status": "ok", "service": "Bug Bounty Cal-Report"}


@app.post("/calculate")
def calculate(req: CalculateRequest) -> dict:
    try:
        return calculate_cvss(req.vector)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/report")
def report(req: ReportRequest) -> dict:
    try:
        result = calculate_cvss(req.vector)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    lines = [
        f"# {req.title}",
        "",
        f"**Target:** {req.target}",
        f"**Severity:** {result['severity']} ({result['base_score']})",
        f"**CVSS Vector:** {result['vector']}",
        "",
        "## Description",
        req.description or "TODO: describe the vulnerability.",
        "",
        "## Impact",
        req.impact or "TODO: describe the impact.",
        "",
        "## Remediation",
        req.remediation or "TODO: describe the fix.",
        "",
    ]
    return {**result, "report": "\n".join(lines)}