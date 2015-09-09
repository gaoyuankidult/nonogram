"""Solvers for nonogram problems operate as coroutines, yielding partial
solutions until they have a complete, correct solution.  A coroutine
may yield None if it has no intermediate solution."""

import rules.nonogram as r


class SolverCoroutine(object):
    """Abstract base class for solvers."""

    def __init__(self, puzzle, initial_solution=None):
        self.puzzle = puzzle
        self.initial_solution = initial_solution or r.NonogramSolution(puzzle)

    def solve(self):
        """This method may yield partial solutions (or None) as much as the
        implementation desires.  If it discovers a complete, correct solution
        then it must yield that solution and return.  If it returns without
        yielding a complete, correct solution, that indicates the solver has
        failed to solve the partial solution, likely because it is impossible.
        """
        raise NotImplementedError(
            "solver did not implement SolverCoroutine.solve")


def test_solver(solver_class, puzzle):
    """Do a trivial test of the given solver class on the given puzzle to see
    that it's working."""
    s = solver_class(puzzle)
    for i in s.solve():
        if i is None:
            print("...")
        else:
            i.debug_print()
    print("Coroutine says that it is done")
    assert i.complete()
    assert i.correct()
