"""Solvers for nonogram problems operate as coroutines, yielding partial
solutions until they have a complete, correct solution.  A coroutine
may yield None if it has no intermediate solution."""

import rules.nonogram as rules


class SolutionNotFound(RuntimeError):
    pass


class SolverCoroutine(object):
    """Abstract base class for solvers."""

    def __init__(self, puzzle, initial_solution=None):
        self.puzzle = puzzle
        self.initial_solution = (initial_solution or
                                 rules.NonogramSolution(puzzle))

    def solve(self):
        """Iteratively solve the puzzle, emitting partial solutions along the
        way.

        This method may yield partial solutions (or None) as much as the
        implementation desires.  If it discovers a complete, correct solution
        then it must yield that solution and return.

        If no solution is possible, raises SolutionNotFound.
        """
        raise NotImplementedError(
            "solver did not implement SolverCoroutine.solve")


def test_solver(solver_class, puzzle):
    """Do a trivial test of the given solver class on the given puzzle to see
    that it's working."""
    solver = solver_class(puzzle)
    solution = None
    for solution in solver.solve():
        if solution is None:
            print("...")
        else:
            solution.debug_print()
    print("Coroutine says that it is done")
    assert solution.complete()
    assert solution.correct()
