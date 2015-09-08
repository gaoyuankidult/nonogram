"""Solvers for nonogram problems operate as coroutines, yielding partial
solutions until they have a complete, correct solution.  A coroutine
may yield None if it has no intermediate solution."""

from rules.nonogram import NonogramPuzzle


class SolverCoroutine(object):
    def solve(self):
        raise NotImplementedError(
            "solver did not implement SolverCoroutine.solve")


def test_solver(solver_class, puzzle):
    """Do a trivial test of the given solver class on the given puzzle to see
    that it's working."""
    s = solver_class(puzzle)
    for i in s.solve():
        if i is None:
            print "..."
        else:
            i.debug_print()
    print "Coroutine says that it is done"
    assert i.complete()
    assert i.correct()
