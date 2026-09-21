
from .puzzle_client import PuzzleClient


class PuzzleSolver:

    def __init__(self, client: PuzzleClient) -> None:
        self._client = client
        self._responses = {}

    def solve(self) -> str:
        n = 2
        exists = False
        while exists is False: 
            responses = self._client.get(n)
            if responses.is_ok():
                for data in responses.value():
                    if data['index'] in self._responses:
                        exists = True
                        break
                    self._responses[data['index']] = data
                n += n
            else:
                return responses.error_message()

        return ' '.join(d['text'] for d in sorted(self._responses.values(), key=lambda d: d['index']))

