"""Solvers for oekaki problems operate as coroutines, yielding partial
solutions until they have a complete, correct solution.  A coroutine
may yield None if it has no intermediate solution."""

from rules.oekaki import OekakiPuzzle


class SolverCoroutine(object):
    def solve(self):
        raise NotImplementedError(
            "solver did not implement SolverCoroutine.solve")


def test_solver(solver_class):
    """Do a trivial test of the given solver class to see that it's working."""
    p = OekakiPuzzle([[1], [1, 1]],
                     [[1], [1], [1]])
    s = solver_class(p)
    for i in s.solve():
        if i is None:
            print "..."
        else:
            i.debug_print()
    print "Coroutine says that it is done"
    assert i.complete()
    assert i.correct()

def demo():
    from solver.brute_force import BruteForceOekakiSolver
    test_solver(BruteForceOekakiSolver)
