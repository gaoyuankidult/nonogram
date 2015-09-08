#!/usr/bin/env python

"""Brief demo of oekaki solving."""

import sys

from rules.oekaki import OekakiPuzzle

easy_puzzle = OekakiPuzzle([[1], [1, 1]],
                           [[1], [1], [1]])

def main(args):
    from solver.solver_coroutine import test_solver
    from solver.brute_force import BruteForceOekakiSolver
    test_solver(BruteForceOekakiSolver, easy_puzzle)

if __name__ == "__main__":
    main(sys.argv)
