#!/usr/bin/env python3

"""Test suite for rules.nonogram."""

import unittest

from rules.nonogram import *
from rules.sample_puzzles import *


class PuzzleErrorTest(unittest.TestCase):
    def test_mismatch_error(self):
        with self.assertRaises(AssertionError):
            NonogramPuzzle("NumberMismatch", [[1], [2]], [[1], [1]])
        with self.assertRaises(AssertionError):
            NonogramPuzzle("NumberMismatch", [[1], [1]], [[1], [2]])


class SolutionErrorTest(unittest.TestCase):
    def test_contradiction(self):
        for solution in all_possible_total_solutions(
                NonogramSolution(contradictory_puzzle)):
            self.assertTrue(solution.complete())
            self.assertFalse(solution.correct())

    def test_ambiguity(self):
        num_solutions = 0
        for solution in all_possible_total_solutions(
                NonogramSolution(ambiguous_puzzle)):
            self.assertTrue(solution.complete())
            if solution.correct():
                num_solutions += 1
        self.assertGreater(num_solutions, 1)


# Obligatory main hook

if __name__ == "__main__":
    unittest.main()
