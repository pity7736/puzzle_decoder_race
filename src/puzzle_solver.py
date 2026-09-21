
import httpx


class PuzzleSolver:

    def __init__(self, http_client: httpx.Client) -> None:
        self._client = http_client
        self._responses = {}

    def solve(self) -> str:
        index = -1
        n = 0
        while True: 
            print(n)
            response = self._client.get(f'http://localhost:8080/fragment?id={n}')
            data = response.json()
            print(data)
            index = data['index']
            if index in self._responses:
                break
            self._responses[data['index']] = data
            n += 1

        print(self._responses)
        text = []
        for data in sorted(self._responses.values(), key=lambda d: d['index']):
            text.append(data['text'])

        print(text)
        return ' '.join(text)

