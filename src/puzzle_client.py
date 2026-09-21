import httpx

class Result[T]:

    def __init__(self, value: T | None, error: str) -> None:
        self._value = value
        self._error = error

    @classmethod
    def ok(cls, value: T) -> 'Result[T]':
        return cls(value, "")

    @classmethod
    def error(cls, error: str) -> 'Result[T]':
        return cls(None, error)

    def is_ok(self) -> bool:
        return not bool(self._error)

    def value(self) -> T:
        assert self._value is not None
        return self._value

    def error_message(self) -> str:
        return self._error


class PuzzleClient:
    
    def __init__(self, http_client: httpx.Client) -> None:
        self._client = http_client
        self._since = 0

    def get(self, limit: int) -> Result[list[dict]]:
        result = []
        for i in range(self._since, limit):
            try:
                response = self._client.get(f'http://localhost:8080/fragment?id={i}')
            except httpx.HTTPError:
                return Result.error('unexpected error occurred')
            else:
               result.append(response.json())
        
        self._since = limit
        return Result.ok(result)

