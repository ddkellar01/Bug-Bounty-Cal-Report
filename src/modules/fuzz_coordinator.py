import concurrent.futures

class FuzzCoordinator:
    """Coordinates concurrent fuzzing tasks across targets."""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def run_campaign(self, targets: list, fuzz_func) -> list:
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_target = {executor.submit(fuzz_func, t): t for t in targets}
            for future in concurrent.futures.as_completed(future_to_target):
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append({"target": future_to_target[future], "error": str(e)})
        return results
