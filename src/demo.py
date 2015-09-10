#!/usr/bin/env python3

"""Brief demo of nonogram solving."""

import sys

from rules.nonogram import NonogramPuzzle

easy_puzzle = NonogramPuzzle([[1], [1, 1]],
                             [[1], [1], [1]])

ambiguous_puzzle = NonogramPuzzle([[1], [1]],
                                  [[1], [1]])

hard_puzzle = NonogramPuzzle(
    # https://commons.wikimedia.org/wiki/File:Paint_by_numbers_Animation.gif
    [[3], [5], [3, 1], [2, 1], [3, 3, 4], [2, 2, 7], [6, 1, 1], [4, 2, 2],
     [1, 1], [3, 1], [6], [2, 7], [6, 3, 1], [1, 2, 2, 1, 1], [4, 1, 1, 3],
     [4, 2, 2], [3, 3, 1], [3, 3], [3], [2, 1]],
    [[2], [1, 2], [2, 3], [2, 3], [3, 1, 1], [2, 1, 1], [1, 1, 1, 2, 2],
     [1, 1, 3, 1, 3], [2, 6, 4], [3, 3, 9, 1], [5, 3, 2], [3, 1, 2, 2],
     [2, 1, 7], [3, 3, 2], [2, 4], [2, 1, 2], [2, 2, 1], [2, 2], [1], [1]])


def main(_):
    # TODO ggould use argparse here.

    from solver.solver_coroutine import test_solver
    from solver.brute_force import BruteForceNonogramSolver

    test_solver(BruteForceNonogramSolver, easy_puzzle)
    test_solver(BruteForceNonogramSolver, ambiguous_puzzle)
    from solver.backward_chain_solver import BackwardChainSolver

    test_solver(BackwardChainSolver, easy_puzzle)
    test_solver(BackwardChainSolver, ambiguous_puzzle)
    test_solver(BackwardChainSolver, hard_puzzle)


if __name__ == "__main__":
    main(sys.argv)
