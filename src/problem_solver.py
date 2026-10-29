from enum import Enum
from typing import Dict, Any

class ProblemTier(Enum):
    EASY = "Easy (Clear / Deterministic)"
    COMPLICATED = "Complicated (Expert Analysis Required)"
    COMPLEX = "Complex (Emergent / Multi-Agent Reasoning)"
    CHAOTIC = "Chaotic (Crisis / Zero-Day Detonation)"

class ProblemSolverEngine:
    """Classifies vulnerabilities into a 4-tier problem-solving architecture."""
    
    @staticmethod
    def classify(finding: Dict[str, Any]) -> ProblemTier:
        impact = finding.get("impact_score", 0.0)
        complexity = finding.get("complexity", "low")
        is_zero_day = finding.get("zero_day", False)
        
        if is_zero_day and impact >= 9.0:
            return ProblemTier.CHAOTIC
        elif complexity == "high" or impact >= 7.0:
            return ProblemTier.COMPLEX
        elif impact >= 4.0:
            return ProblemTier.COMPLICATED
        else:
            return ProblemTier.EASY
