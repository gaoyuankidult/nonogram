"""Module that implements the rules of the Nonogram puzzle game.

An Nonogram puzzle presents a user with a blank grid.  Each row and each
column has a list of run lengths.  The objective is to fill the grid with
marked and unmarked squares so that in each run and each column the runs of
contiguous marked squares have the lengths listed.

For instance, this is a valid puzzle:
 NonogramPuzzle([[1],[1,1],[2],[3],[3],[1,1]],[[1,3],[1,3],[5]])

     1  1
     3  3  5
    +--------
1   |   ##
1 1 |##    ##
2   |   ## ##
3   |## ## ##
3   |## ## ##
1 1 |##    ##

The column run lengths and row run lengths must sum to the same number.

Some Nonogram can be undecidable (consider [[1][1]],[[1][1]]) or inconsistent
(consider [[1,1],[2]],[[2],[0],[2]]).
"""

import copy


class NonogramPuzzle(object):
    """Class that implements a blank puzzle.

    This is an immutable object, because it is unlikely that mutating it would
    be valid and likely it would create bugs.
    """

    def __init__(self, name, row_run_counts, column_run_counts):
        self._name = name
        self._row_run_counts = tuple(tuple(run) for run in row_run_counts)
        self._col_run_counts = tuple(tuple(run) for run in column_run_counts)
        self.validate()

    def validate(self):
        """Check the validity of a given puzzle (ie, that the run counts are
        at all sensible, not that it is uniquely solvable)."""
        row_total = sum(sum(runs) for runs in self._row_run_counts)
        col_total = sum(sum(runs) for runs in self._col_run_counts)
        assert row_total == col_total

        min_width = max(sum(runs) + len(runs)
                        for runs in self.row_run_counts) - 1
        min_height = max(sum(runs) + len(runs)
                         for runs in self.col_run_counts) - 1
        assert self.width >= min_width, \
            "Puzzle width %d cannot fit runs %d" % (self.width, min_width)
        assert self.height >= min_height, \
            "Puzzle height %d cannot fit runs %d" % (self.height, min_height)

    @property
    def name(self):
        """The name of the puzzle; may be None."""
        return self._name

    @property
    def row_run_counts(self):
        """The list of row run counts."""
        return self._row_run_counts

    @property
    def col_run_counts(self):
        """The list of column run counts."""
        return self._col_run_counts

    @property
    def width(self):
        """The width of the puzzle"""
        return len(self.col_run_counts)

    @property
    def height(self):
        """The height of the puzzle"""
        return len(self.row_run_counts)

    # Helper routines for ascii rendering
    @staticmethod
    def ascii_single_row_header(run_counts, pad_to=None):
        """Return the leading string of row run counts that would appear to
        the left of a grid row when a puzzle is printed out.  If @p pad_to is
        provided, pads the returned string to that width using leading spaces.
        """
        content = " ".join(str(run) for run in run_counts)
        padding = ("" if pad_to is None or len(content) > pad_to else
                   " " * (pad_to - len(content) - 1))
        return padding + content + " |"

    def ascii_single_row_header_width(self, run_counts):
        """Return the width of a row run counts string, as would be returned
        by ascii_single_row_header, for the given @p run_counts"""
        return len(self.ascii_single_row_header(run_counts))

    def ascii_max_row_header_width(self):
        """Return the maximum value of ascii_single_row_header_width for the
        whole puzzle, ie, the width to which all row run count headers must be
        padded."""
        return max(self.ascii_single_row_header_width(run_counts)
                   for run_counts in self.row_run_counts)

    def ascii_nth_single_row_header(self, n):
        """Return an appropriately padded row header for row @p n."""
        pad_to = self.ascii_max_row_header_width()
        return self.ascii_single_row_header(self.row_run_counts[n],
                                            pad_to=pad_to)

    def ascii_col_header_string(self):
        """Return a string showing the column run counts, arranged vertically,
        as would appear above the columns in a printed puzzle."""
        result = ""
        row_padding = " " * self.ascii_max_row_header_width()
        num_header_rows = max(len(run_counts)
                              for run_counts in self.col_run_counts)
        for y in range(num_header_rows):
            result += row_padding
            for x in range(len(self.col_run_counts)):
                run_counts = self.col_run_counts[x]
                idx = y - (num_header_rows - len(run_counts))
                if idx < 0:
                    result += "   "
                    continue
                result += "%3d" % run_counts[idx]
            result += "\n"
        result += row_padding + "+" + ("---" * len(self.col_run_counts))
        return result

    def debug_print(self):
        """Print a human-readable representation of the puzzle to stdout."""
        print(self.ascii_col_header_string())
        for n in range(len(self.row_run_counts)):
            print(self.ascii_nth_single_row_header(n))


MARKED, UNMARKED, UNKNOWN = "##", ". ", "  "


def satisfies(cells, run_count_list):
    """Return True if the list of MARKED or UNMARKED cells in @p cells
    satisfies the list of runs in @p run_count_list."""
    if UNKNOWN in cells:
        raise AttributeError("UNKNOWN in satisfies() call %s" % cells)
    if not run_count_list:
        # No more runs; the remaining cells had better be empty.
        return all(cell == UNMARKED for cell in cells)
    if not cells:
        return run_count_list == [0]  # Last run just finished.
    new_run_count_list = list(run_count_list)
    if cells[0] == UNMARKED:
        if new_run_count_list[0] == 0:
            # Just finished a run; mark it off.
            new_run_count_list = new_run_count_list[1:]
        return satisfies(cells[1:], new_run_count_list)
    elif cells[0] == MARKED:
        if new_run_count_list[0] == 0:
            # Overran this run.
            return False
        return satisfies(cells[1:],
                         [run_count_list[0] - 1] + new_run_count_list[1:])


class NonogramSolution(object):
    """Represents a partial or complete solution to an NonogramPuzzle.
    Internal coordinates are X left-to-right, Y top-to-bottom."""

    def __init__(self, puzzle):
        self._puzzle = puzzle
        self.cells = [[UNKNOWN] * puzzle.height for _ in range(puzzle.width)]

    @property
    def puzzle(self):
        """The puzzle for which this object represents a solution."""
        return self._puzzle

    def row(self, y):
        """Return the @p y th row of the solution."""
        return [self.cells[x][y]
                for x in range(self.puzzle.width)]

    @property
    def rows(self):
        """A list of the rows of this solution."""
        for y in range(self._puzzle.height):
            yield self.row(y)

    def column(self, x):
        """Return the @p x th row of the solution."""
        return [self.cells[x][y]
                for y in range(self.puzzle.height)]

    @property
    def columns(self):
        """A list of the columns of this solution."""
        for x in range(self._puzzle.width):
            yield self.column(x)

    def complete(self):
        """Return True iff this is a complete solution (no UNKNOWN cells)."""
        return not any(cell == UNKNOWN for row in self.cells for cell in row)

    def correct(self):
        """Return True iff every row or column lacking an UNKNOWN cell
        satisfies its row or column row count list.

        DOES NOT check if the list can be satisfied for rows and columns
        with UNKNOWN even if the unknown is irrelevant.
        """
        for x in range(self.puzzle.width):
            col = self.column(x)
            if UNKNOWN in col:
                continue
            if not satisfies(col, self.puzzle.col_run_counts[x]):
                return False
        for y in range(self.puzzle.height):
            row = self.row(y)
            if UNKNOWN in row:
                continue
            if not satisfies(row, self.puzzle.row_run_counts[y]):
                return False
        return True

    def mark(self, *mark_coords):
        """Set the cells at the indicated coordinates (which must be UNKNOWN)
        to MARKED."""
        for (x, y) in mark_coords:
            assert self.cells[x][y] == UNKNOWN
            self.cells[x][y] = MARKED

    def unmark(self, *unmark_coords):
        """Set the cells at the indicated coordinates (which must be UNKNOWN)
        to UNMARKED."""
        for (x, y) in unmark_coords:
            assert self.cells[x][y] == UNKNOWN
            self.cells[x][y] = UNMARKED

    def clone(self):
        """Returns a copy of the solution.

        Utility method to avoid requiring solvers to copy.deepcopy solutions
        constantly."""
        new_soln = NonogramSolution(self.puzzle)
        new_soln.cells = copy.deepcopy(self.cells)
        return new_soln

    def debug_print(self):
        """Print a human-readable representation of this solution to stdout.
        """
        print(self.puzzle.ascii_col_header_string())
        for y in range(self.puzzle.height):
            content = ' '.join(self.cells[x][y]
                               for x in range(self.puzzle.width))
            print(self.puzzle.ascii_nth_single_row_header(y) + " " + content)
