import httpx

from src.puzzle_client import PuzzleClient
from src.puzzle_solver import PuzzleSolver



if __name__ == '__main__':
    solver = PuzzleSolver(PuzzleClient(httpx.Client()))
    print(solver.solve())

