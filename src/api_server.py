from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.modules.cvss_calculator import calculate_cvss
from src.problem_solver import ProblemSolverEngine

app = FastAPI(title="BugBounty-Cal-Report API", version="1.0.0")

class AuditRequest(BaseModel):
    target: str
    impact_score: float
    complexity: str = "high"
    zero_day: bool = False
    vector: str = "AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N"

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "bug-bounty-cal-report"}

@app.post("/api/v1/audit")
def run_api_audit(payload: AuditRequest):
    score, severity = calculate_cvss(payload.vector)
    tier = ProblemSolverEngine.classify(payload.dict())
    return {
        "target": payload.target,
        "cvss_score": score,
        "severity": severity,
        "problem_tier": tier.value,
        "status": "completed"
    }
