"""A brute force solver for nonogram problems.

Simple considers every possible marking combination for every UNKNOWN cell
until one comes up correct.
"""

# TODO ggould figure out why pycharm dislikes doing these as local imports.
from solver.solver_coroutine import SolverCoroutine
from rules.nonogram import NonogramSolution, all_possible_total_solutions

class BruteForceNonogramSolver(SolverCoroutine):
    """A class for solving nonogram problems.  There are no intermediate
    results, so the coroutine does not return any but instead yields None
    after a certain quantity of computation."""

    def __init__(self, puzzle, initial_solution=None):
        super(BruteForceNonogramSolver, self).__init__(
            puzzle, initial_solution)

    def solve(self):
        # See superclass docstring.
        yield self.initial_solution
        for solution in all_possible_total_solutions(
                NonogramSolution(self.puzzle)):
            assert solution.complete()
            if solution.correct():
                yield solution
