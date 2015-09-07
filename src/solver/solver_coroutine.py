"""Solvers for oekaki problems operate as coroutines, yielding partial
solutions until they have a complete, correct solution, or failing
and returning None."""

from rules.oekaki import OekakiPuzzle

class SolverCoroutine(object):
	def solve():
		raise NotImplementedError(
		    "solver did not implement SolverCoroutine.solve")


def test_solver(solver_class):
	"""Do a trivial test of the given solver class to see that it's working."""
	p = OekakiPuzzle([[1], [1, 1]],
	                 [[1], [1], [1]])
	s = solver_class(p)
	for i in s.solve():
		i.debug_print()
	assert i.complete()
	assert i.correct()
