import httpx
import pytest

from src.puzzle_client import PuzzleClient
from src.puzzle_solver import PuzzleSolver

responses = (
    httpx.Response(200, json={'id': 0, 'index': 0, 'text': 'hello'}),
    httpx.Response(200, json={'id': 1, 'index': 2, 'text': 'world'}),
    httpx.Response(200, json={'id': 2, 'index': 1, 'text': 'crazy'}),
    httpx.Response(200, json={'id': 3, 'index': 0, 'text': 'hello'}),
)

iter_responses = iter(responses)
calls = []

def mock_handler(request: httpx.Request) -> httpx.Response:
    calls.append(request)
    return next(iter_responses)


@pytest.mark.asyncio
async def test_solver_should_stop_when_index_exists():
    client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))
    solver = PuzzleSolver(PuzzleClient(client), limit=4)

    result = await solver.solve()
    
    assert len(calls) == 4
    assert result == 'hello crazy world'


@pytest.mark.asyncio
async def test_solver_should_handle_connection_error():
    def error_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused")

    client = httpx.AsyncClient(transport=httpx.MockTransport(error_handler))
    solver = PuzzleSolver(PuzzleClient(client))

    result = await solver.solve()

    assert result == 'unexpected error occurred'

