"""Module that implements the rules of the Oekaki puzzle game.

An Oekaki puzzle presents a user with a blank grid.  Each row and each column
has a list of run lengths.  The objective is to fill the grid with marked and
unmarked squares so that in each run and each column the runs of contiguous
marked squares have the lengths listed.

For instance, this is a valid puzzle:
 OekakiPuzzle([[1],[1,1],[2],[3],[3],[1,1]],[[1,3],[1,3],[5]])

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

Some Oekaki can be undecidable (consider [[1][1]],[[1][1]]) or inconsistent
(consider [[1,1],[2]],[[2],[0],[2]]).
"""


class OekakiPuzzle(object):
    """Class that implements a blank puzzle.

    This is an immutable object, because it is unlikely that mutating it would
    be valid and likely it would create bugs.
    """

    def __init__(self, row_run_counts, column_run_counts):
        self._row_run_counts = tuple(tuple(run) for run in row_run_counts)
        self._col_run_counts = tuple(tuple(run) for run in column_run_counts)
        self.validate()

    def validate(self):
        row_total = sum(sum(runs) for runs in self._row_run_counts)
        col_total = sum(sum(runs) for runs in self._col_run_counts)
        assert row_total == col_total

        min_width = max(sum(runs) + len(runs)
                        for runs in self.row_run_counts) - 1
        min_height = max(sum(runs) + len(runs)
                         for runs in self.col_run_counts) - 1
        assert self.width >= min_width, \
            "Puzzle width %d cannot fit runs %d" % (self.width, min_width)
        assert self.height >= min_height

    @property
    def row_run_counts(self):
        return self._row_run_counts

    @property
    def col_run_counts(self):
        return self._col_run_counts

    @property
    def width(self):
        return len(self.col_run_counts)

    @property
    def height(self):
        return len(self.row_run_counts)

    # Helper routines for ascii rendering
    def ascii_single_row_header(self, run_counts, pad_to=None):
        content = " ".join(str(run) for run in run_counts)
        padding = ("" if pad_to is None or len(content) > pad_to else
                   " " * (pad_to - len(content) - 1))
        return padding + content + " |"

    def ascii_single_row_header_width(self, run_counts):
        return len(self.ascii_single_row_header(run_counts))

    def ascii_max_row_header_width(self):
        return max(self.ascii_single_row_header_width(run_counts)
                   for run_counts in self.row_run_counts)

    def ascii_nth_single_row_header(self, n):
        pad_to = self.ascii_max_row_header_width()
        return self.ascii_single_row_header(self.row_run_counts[n],
                                            pad_to=pad_to)

    def ascii_col_header_string(self):
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
        print self.ascii_col_header_string()
        for n in range(len(self.row_run_counts)):
            print self.ascii_nth_single_row_header(n)


MARKED, UNMARKED, UNKNOWN = "##", " .", "??"


def satisfies(cells, run_count_list):
    """Returns True if the list of MARKED or UNMARKED cells in @p cells
    satisfies the lits of runs in @p run_count_list."""
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


class OekakiSolution(object):
    """Represents a partial or complete solution to an OekakiPuzzle.
    Internal coordinates are X left-to-right, Y top-to-bottom."""

    def __init__(self, puzzle):
        self._puzzle = puzzle
        self.cells = [[UNKNOWN] * puzzle.height for _ in range(puzzle.width)]

    @property
    def puzzle(self):
        return self._puzzle

    def row(self, y):
        """Returns the @p y th row of the solution."""
        return [self.cells[x][y]
                for x in range(self.puzzle.width)]

    def column(self, x):
        """Returns the @p x th row of the solution."""
        return [self.cells[x][y]
                for y in range(self.puzzle.height)]

    def complete(self):
        """Returns True iff this is a complete solution (no UNKNOWN cells).
        """
        return not any(cell == UNKNOWN for row in self.cells for cell in row)

    def correct(self):
        """Returns True iff every row or column lacking an UNKNOWN cell
        adheres to its row or column row count list.

        DOES NOT check if the list can be satisfied for rows and columns
        with UNKNOWNs even if the unknown is irrelevant.
        """
        for x in range(self.puzzle.width):
            col = self.column(x)
            if UNKNOWN in col: continue
            if not satisfies(col, self.puzzle.col_run_counts[x]):
                return False
        for y in range(self.puzzle.height):
            row = self.row(y)
            if UNKNOWN in row: continue
            if not satisfies(row, self.puzzle.row_run_counts[y]):
                return False
        return True

    def unknown_cell_coordinates(self):
        """Return [(x,y), ...] for every (x,y) pair that locates a cell whose
        value is UNKNOWN.
        """
        return [(x, y)
                for x in range(self.puzzle.width)
                for y in range(self.puzzle.height)
                if self.cells[x][y] == UNKNOWN]

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

    def debug_print(self):
        print self.puzzle.ascii_col_header_string()
        for y in range(self.puzzle.height):
            content = ' '.join(self.cells[x][y]
                               for x in range(self.puzzle.width))
            print self.puzzle.ascii_nth_single_row_header(y) + " " + content
