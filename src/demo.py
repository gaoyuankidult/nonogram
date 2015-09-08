#!/usr/bin/env python

"""Brief demo of oekaki solving."""

import sys

from rules.oekaki import OekakiPuzzle

easy_puzzle = OekakiPuzzle([[1], [1, 1]],
                           [[1], [1], [1]])

ambiguous_puzzle = OekakiPuzzle([[1], [1]],
                                [[1], [1]])

def main(args):
    from solver.solver_coroutine import test_solver
    from solver.brute_force import BruteForceOekakiSolver
    test_solver(BruteForceOekakiSolver, easy_puzzle)
    test_solver(BruteForceOekakiSolver, ambiguous_puzzle)
    from solver.backward_chain_solver import BackwardChainSolver
    test_solver(BackwardChainSolver, easy_puzzle)
    test_solver(BackwardChainSolver, ambiguous_puzzle)

if __name__ == "__main__":
    main(sys.argv)
