import asyncio
import os

import httpx

from src.puzzle_client import PuzzleClient
from src.puzzle_solver import PuzzleSolver



if __name__ == '__main__':
    base_url = os.getenv('PUZZLE_SERVER_URL', 'http://localhost:8080')
    solver = PuzzleSolver(PuzzleClient(httpx.AsyncClient(), base_url))
    print(asyncio.run(solver.solve()))

