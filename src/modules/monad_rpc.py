import requests

class MonadRPCClient:
    """JSON-RPC client for interacting with Monad network nodes."""
    
    def __init__(self, rpc_url: str = "https://rpc.monad.xyz"):
        self.rpc_url = rpc_url

    def get_block_number(self) -> int:
        payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
        try:
            resp = requests.post(self.rpc_url, json=payload, timeout=5)
            result = resp.json().get("result")
            return int(result, 16) if result else 0
        except Exception:
            return 0
