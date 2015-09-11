#!/usr/bin/env python3

"""Test suite for NonogramPuzzle."""

import unittest

from rules.nonogram import NonogramPuzzle


class PuzzleErrorTest(unittest.TestCase):
    def test_mismatch_error(self):
        with self.assertRaises(AssertionError):
            NonogramPuzzle("NumberMismatch", [[1], [2]], [[1], [1]])
        with self.assertRaises(AssertionError):
            NonogramPuzzle("NumberMismatch", [[1], [1]], [[1], [2]])


# Obligatory main hook

if __name__ == "__main__":
    unittest.main()
