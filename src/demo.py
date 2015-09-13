#!/usr/bin/env python3

"""Brief demo of nonogram solving."""

import argparse
import sys

from rules.sample_puzzles import puzzles
from solver.solver_coroutine import test_solver

from solver.brute_force import BruteForceNonogramSolver
from solver.backward_chain_solver import BackwardChainSolver

def main(args):
    parser = argparse.ArgumentParser(description=__doc__, prog=args[0])
    parser.add_argument("-l", "--list", action="store_true",
                        help="List all available tests.")
    parser.add_argument("-q", "--quick",
                        type=int, action="append", metavar="TEST_NUM",
                        help="Run one specific test.")
    options = parser.parse_args(args[1:])

    tests = [  # (solver, puzzle) pairs indicating tests to run
             (BruteForceNonogramSolver, puzzles['easy_puzzle']),
             (BruteForceNonogramSolver, puzzles['ambiguous_puzzle']),
             (BackwardChainSolver, puzzles['easy_puzzle']),
             (BackwardChainSolver, puzzles['ambiguous_puzzle']),
             (BackwardChainSolver, puzzles['hard_picture']),
            ]
    tests_to_run = []

    if options.quick:
        tests_to_run = [tests[i] for i in options.quick]
    else:
        tests_to_run = tests

    if options.list:
        for (test_num, (solver, puzzle)) in enumerate(tests):
            print(str(test_num) + ":", solver.__name__, puzzle.name)
        return

    for (solver, puzzle) in tests_to_run:
        test_solver(solver, puzzle)


if __name__ == "__main__":
    main(sys.argv)
