"""Sample nonogram puzzles for testing.
"""

from rules.nonogram import NonogramPuzzle


puzzles = {}


# This puzzle is trivially solvable through deduction.
puzzles["easy_puzzle"] = easy_puzzle = NonogramPuzzle(
    "Easy Puzzle",
    [[1], [1, 1]],
    [[1], [1], [1]])


# This puzzle has multiple legal solutions.
puzzles["ambiguous_puzzle"] = ambiguous_puzzle = NonogramPuzzle(
    "Ambiguous Puzzle",
    [[1], [1]],
    [[1], [1]])


# This puzzle cannot be solved through straightforward deduction and requires
# several layers of hypothesis to solve.
puzzles["hard_picture"] = hard_puzzle = NonogramPuzzle(
    "Hard picture",
    # https://commons.wikimedia.org/wiki/File:Paint_by_numbers_Animation.gif
    [[3], [5], [3, 1], [2, 1], [3, 3, 4], [2, 2, 7], [6, 1, 1], [4, 2, 2],
     [1, 1], [3, 1], [6], [2, 7], [6, 3, 1], [1, 2, 2, 1, 1], [4, 1, 1, 3],
     [4, 2, 2], [3, 3, 1], [3, 3], [3], [2, 1]],
    [[2], [1, 2], [2, 3], [2, 3], [3, 1, 1], [2, 1, 1], [1, 1, 1, 2, 2],
     [1, 1, 3, 1, 3], [2, 6, 4], [3, 3, 9, 1], [5, 3, 2], [3, 1, 2, 2],
     [2, 1, 7], [3, 3, 2], [2, 4], [2, 1, 2], [2, 2, 1], [2, 2], [1], [1]])

