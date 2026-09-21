
from .puzzle_client import PuzzleClient


class PuzzleSolver:

    def __init__(self, client: PuzzleClient, limit: int = 30) -> None:
        self._client = client
        self._responses = {}
        self._limit = limit

    async def solve(self) -> str:
        exists = False
        while exists is False: 
            responses = await self._client.get(self._limit)
            if responses.is_ok():
                for data in responses.value():
                    if data['index'] in self._responses:
                        exists = True
                        break
                    self._responses[data['index']] = data
                self._limit += self._limit
            else:
                return responses.error_message()

        return ' '.join(d['text'] for d in sorted(self._responses.values(), key=lambda d: d['index']))

