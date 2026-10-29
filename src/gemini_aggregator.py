import os
from google import genai
from google.genai import types

class GeminiGrandReportBot:
    """Aggregates sub-reports from all feature modules and synthesizes a Grand Executive Report."""
    
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY", "dummy-key")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-pro"

    def synthesize_grand_report(self, sub_reports: dict) -> str:
        prompt = f"""
        You are the Lead Security Architect and AI Auditor. Synthesize the following component reports into a unified, professional Grand Vulnerability & Compliance Report.
        
        Component Reports:
        1. CVSS & Severity Assessment: {sub_reports.get('cvss', 'N/A')}
        2. Web/API Vulnerability Scanner: {sub_reports.get('web_scan', 'N/A')}
        3. EVM/Monad Fuzzer & Contract Analysis: {sub_reports.get('evm_fuzz', 'N/A')}
        4. eBPF Sandbox Telemetry: {sub_reports.get('sandbox', 'N/A')}
        5. ISO/IEC Compliance Audit (iso-iecx): {sub_reports.get('iso_audit', 'N/A')}
        6. Operational Problem Tier: {sub_reports.get('tier', 'N/A')}

        Structure the output with an Executive Summary, Consolidated Findings Table, ISO/IEC Compliance Status, and Risk-Prioritized Remediation Roadmap.
        """
        
        try:
            config = types.GenerateContentConfig(
                temperature=0.2,
                thinking_config=types.ThinkingConfig(thinking_budget=4096)
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            return f"# Grand Report (Simulated Synthesis)\n\nError connecting to Gemini API: {e}\n\nSub-reports gathered successfully: {list(sub_reports.keys())}"
