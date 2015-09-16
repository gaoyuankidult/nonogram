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


# Obligatory main hook

if __name__ == "__main__":
    unittest.main()
