import argparse
import sys
from src.problem_solver import ProblemSolverEngine, ProblemTier
from src.gemini_thinking import GeminiExtendedThinkingEngine
from src.modules.cvss_calculator import calculate_cvss
from src.modules.report_generator import generate_report

def main():
    parser = argparse.ArgumentParser(description="Bug Bounty Calculator & Automated Report Engine")
    parser.add_argument("--target", required=True, help="Target application, endpoint, or contract")
    parser.add_argument("--vector", default="AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N", help="CVSS v3.1 vector string")
    args = parser.parse_args()

    print(f"[*] Initializing BugBounty-Cal-Report engine against target: {args.target}")
    
    score, severity = calculate_cvss(args.vector)
    print(f"[+] Computed CVSS Score: {score} ({severity})")

    finding_payload = {"target": args.target, "impact_score": score, "complexity": "high", "zero_day": score >= 9.0}
    tier = ProblemSolverEngine.classify(finding_payload)
    print(f"[+] Problem Classification Tier: {tier.value}")

    thinking_engine = GeminiExtendedThinkingEngine()
    analysis = thinking_engine.analyze(f"Analyze vulnerability on target {args.target} with score {score}.")
    print(f"\n[+] Gemini Reasoning Output:\n{analysis[:300]}...\n")

    report = generate_report(args.target, args.vector, score, severity, tier.value)
    print("[+] Report generated successfully.")

if __name__ == "__main__":
    main()
