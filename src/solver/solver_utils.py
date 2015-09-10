"""General-purpose solver utilities that might be useful to more than one
solver."""

import rules.nonogram as r


def unknown_cell_coordinates(solution):
    """Return [(x,y), ...] for every (x,y) pair in @p solution that locates
    a cell whose value is UNKNOWN.
    """
    return [(x, y)
            for x in range(solution.puzzle.width)
            for y in range(solution.puzzle.height)
            if solution.cells[x][y] == r.UNKNOWN]


def _partitions(total, length):
    """Generate all lists of nonnegative integers of length @p length that sum
    to @p total."""
    if length == 0:
        if total > 0:
            return
    if total == 0:
        yield [0] * length
        return

    for first in range(total + 1):
        shorter_partitions = _partitions(total - first, length - 1)
        partitions = ([first] + shorter_partition
                      for shorter_partition in shorter_partitions)
        for p in partitions:
            yield p


def all_legal_lines(run_counts, current_line):
    """Return a set of all complete lines (lists of MARKED/UNMARKED)
    that have the given run counts for marked cells and change the
    state only of UNKNOWN cells in current_line."""
    num_marked_runs = len(run_counts)
    num_unmarked_runs = len(run_counts) + 1
    num_unmarked_cells = len(current_line) - sum(run_counts)
    num_unallocated_unmarks = num_unmarked_cells - (num_marked_runs - 1)
    assert num_unallocated_unmarks >= 0

    # A run of unmarked cells may occur at the beginning and end of the line
    # and must occur between each run.  Thus num_marked_runs - 1 unmarked
    # cells are already spoken for; the remaining unmarks can be allocated
    # in any way over the remaining unmarked runs.
    for partition in _partitions(num_unallocated_unmarks, num_unmarked_runs):
        line = [r.UNMARKED] * partition[0]
        for i in range(num_marked_runs):
            line += [r.MARKED] * run_counts[i]
            line += [r.UNMARKED] * (partition[i + 1] + 1)
        line.pop()
        assert len(line) == len(current_line)
        # Filter out any allocation inconsistent with current_line.
        for i in range(len(current_line)):
            if current_line[i] != r.UNKNOWN:
                if current_line[i] != line[i]:
                    break
        else:
            # Did not error out.
            yield line
