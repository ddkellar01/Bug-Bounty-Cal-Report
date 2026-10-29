class SolidityContractAnalyzer:
    """Static AST and pattern analyzer for smart contract vulnerabilities."""
    
    @staticmethod
    def scan_source(source_code: str) -> list:
        findings = []
        if "call.value(" in source_code or ".transfer(" in source_code:
            findings.append({"type": "Reentrancy Risk", "severity": "High"})
        if "tx.origin" in source_code:
            findings.append({"type": "Auth Bypass via tx.origin", "severity": "Medium"})
        return findings
