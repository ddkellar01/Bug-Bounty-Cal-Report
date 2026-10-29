import requests

class WebVulnerabilityScanner:
    """Scans web and API endpoints for common authorization and injection flaws."""
    
    def __init__(self, target_url: str):
        self.target_url = target_url

    def probe_endpoint(self, path: str) -> dict:
        url = f"{self.target_url.rstrip('/')}/{path.lstrip('/')}"
        try:
            resp = requests.get(url, timeout=5)
            return {"url": url, "status_code": resp.status_code, "vulnerable": resp.status_code == 200}
        except Exception as e:
            return {"url": url, "error": str(e), "vulnerable": False}
