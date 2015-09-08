#!/usr/bin/env python

"""Brief demo of nonogram solving."""

import sys

from rules.nonogram import NonogramPuzzle

easy_puzzle = NonogramPuzzle([[1], [1, 1]],
                             [[1], [1], [1]])

ambiguous_puzzle = NonogramPuzzle([[1], [1]],
                                  [[1], [1]])

def main(args):
    from solver.solver_coroutine import test_solver
    from solver.brute_force import BruteForceNonogramSolver
    test_solver(BruteForceNonogramSolver, easy_puzzle)
    test_solver(BruteForceNonogramSolver, ambiguous_puzzle)
    from solver.backward_chain_solver import BackwardChainSolver
    test_solver(BackwardChainSolver, easy_puzzle)
    test_solver(BackwardChainSolver, ambiguous_puzzle)

if __name__ == "__main__":
    main(sys.argv)
