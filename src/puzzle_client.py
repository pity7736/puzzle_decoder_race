import asyncio

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
    
    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._client = http_client
        self._since = 0

    async def get(self, limit: int) -> Result[list[dict]]:
        tasks = []
        for i in range(self._since, limit):
            tasks.append(self._do_request(i))

        self._since = limit
        task_result = await asyncio.gather(*tasks) 
        for result in task_result:
            if not result:
                return Result.error("unexpected error occurred")

        return Result.ok(task_result)

    async def _do_request(self, i) -> dict | None:
        try:
            response = await self._client.get(f'http://localhost:8080/fragment?id={i}')
        except httpx.HTTPError:
            return None
        else:
           return response.json()
        


