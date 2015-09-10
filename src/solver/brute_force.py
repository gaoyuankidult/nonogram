"""A brute force solver for nonogram problems.

Simple considers every possible marking combination for every UNKNOWN cell
until one comes up correct.
"""

from .solver_utils import unknown_cell_coordinates
from .solver_coroutine import SolverCoroutine


class BruteForceNonogramSolver(SolverCoroutine):
    """A class for solving nonogram problems.  There are no intermediate
    results, so the coroutine does not return any but instead yields None
    after a certain quantity of computation."""

    def __init__(self, puzzle, initial_solution=None):
        super(BruteForceNonogramSolver, self).__init__(
            puzzle, initial_solution)

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
            solution = self.initial_solution.clone()
            solution.mark(*marks)
            solution.unmark(*unmarks)
            assert solution.complete()
            if solution.correct():
                yield solution
                return
            else:
                yield None
        yield None
