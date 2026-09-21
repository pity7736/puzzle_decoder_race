import time

import httpx
import pytest

from src.puzzle_client import PuzzleClient
from src.puzzle_solver import PuzzleSolver


@pytest.mark.asyncio
async def test_right_message():
    solver = PuzzleSolver(PuzzleClient(httpx.AsyncClient()))

    t = time.monotonic()
    message = await solver.solve()

    assert time.monotonic() - t < 1
    assert message == 'hello world quick brown fox jumps over lazy dog you have to call all request at same time if you want to see the puzzle fragments fast enough'

