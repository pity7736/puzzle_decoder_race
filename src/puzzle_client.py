import httpx


class PuzzleClient:
    
    def __init__(self, http_client: httpx.Client) -> None:
        self._client = http_client
        self._since = 0

    def get(self, limit: int) -> list[dict]:
        result = []
        for i in range(self._since, limit):
            response = self._client.get(f'http://localhost:8080/fragment?id={i}')
            result.append(response.json())
        
        self._since = limit
        return result

