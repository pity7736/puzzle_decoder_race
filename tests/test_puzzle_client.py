import httpx
import pytest

from src.puzzle_client import PuzzleClient

data = [
    {'id': 0, 'index': 0, 'text': 'hello'},
    {'id': 1, 'index': 2, 'text': 'world'},
    {'id': 2, 'index': 1, 'text': 'crazy'}
]

responses = (
    httpx.Response(200, json=data[0]),
    httpx.Response(200, json=data[1]),
    httpx.Response(200, json=data[2]),
)

iter_responses = iter(responses)
calls = []

def mock_handler(request: httpx.Request) -> httpx.Response:
    calls.append(request)
    return next(iter_responses)

@pytest.mark.asyncio
async def test_make_n_requests():
    http_client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    client = PuzzleClient(http_client)
    result = await client.get(3)

    assert result.value() == data

@pytest.mark.asyncio
async def test_consecutive_gets_fetch_correct_ranges():
    all_data = [{'id': i} for i in range(12)]
    resps = iter([httpx.Response(200, json=d) for d in all_data])

    def handler(request: httpx.Request) -> httpx.Response:
        return next(resps)

    client = PuzzleClient(httpx.AsyncClient(transport=httpx.MockTransport(handler)))

    first = await client.get(2)
    second = await client.get(4)
    third = await client.get(8)

    assert first.value() == [{'id': 0}, {'id': 1}]
    assert second.value()== [{'id': 2}, {'id': 3}]
    assert third.value() == [{'id': 4}, {'id': 5}, {'id': 6}, {'id': 7}]

