import os
from jinja2 import Template

def generate_report(target: str, vector: str, score: float, severity: str, tier: str, output_path: str = "vulnerability_report.md") -> str:
    template_content = """# Vulnerability Disclosure Report
- **Target:** {{ target }}
- **CVSS Vector:** {{ vector }}
- **Base Score:** {{ score }} ({{ severity }})
- **Problem Tier:** {{ tier }}

## Executive Summary
This finding was automatically assessed and classified through the BugBounty-Cal-Report reasoning pipeline.
"""
    t = Template(template_content)
    rendered = t.render(target=target, vector=vector, score=score, severity=severity, tier=tier)
    
    with open(output_path, "w") as f:
        f.write(rendered)
    return output_path
