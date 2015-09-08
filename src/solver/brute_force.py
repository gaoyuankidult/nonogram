"""A brute force solver for oekaki problems.

Simple considers every possible marking combination for every UNKNOWN cell
until one comes up correct.
"""

import copy

from rules.oekaki import OekakiSolution

from solver_utils import unknown_cell_coordinates
from solver_coroutine import SolverCoroutine


class BruteForceOekakiSolver(SolverCoroutine):
    """A class for solving oekaki problems.  There are no intermediate
    results, so the coroutine does not return any but instead yields
    after a certain quantity of computation."""

    def __init__(self, puzzle, initial_solution=None):
        self.puzzle = puzzle
        self.initial_solution = initial_solution or OekakiSolution(puzzle)

    def solve(self):
        yield self.initial_solution
        unknown_coords = unknown_cell_coordinates(self.initial_solution)
        for case in range(1 << len(unknown_coords)):
            marks = [unknown_coords[i]
                     for i in range(len(unknown_coords))
                     if case & (1 << i)]
            unmarks = [unknown_coords[i]
                       for i in range(len(unknown_coords))
                       if not (case & (1 << i))]
            solution = copy.deepcopy(self.initial_solution)
            solution.mark(*marks)
            solution.unmark(*unmarks)
            assert solution.complete()
            if solution.correct():
                yield solution
                return
            else:
                yield None
        yield None
