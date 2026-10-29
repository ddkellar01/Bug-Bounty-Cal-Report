import pytest
from src.modules.cvss_calculator import calculate_cvss
from src.problem_solver import ProblemSolverEngine, ProblemTier

def test_cvss_calculation():
    score, severity = calculate_cvss("AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N")
    assert score > 0.0
    assert severity in ["Low", "Medium", "High", "Critical"]

def test_problem_classification():
    finding = {"impact_score": 8.8, "complexity": "high", "zero_day": False}
    tier = ProblemSolverEngine.classify(finding)
    assert tier == ProblemTier.COMPLEX
