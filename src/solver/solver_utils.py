"""General-purpose solver utilities that might be useful to more than one
solver."""

import rules.oekaki as r

def unknown_cell_coordinates(solution):
    """Return [(x,y), ...] for every (x,y) pair in @p solution that locates
    a cell whose value is UNKNOWN.
    """
    return [(x, y)
            for x in range(solution.puzzle.width)
            for y in range(solution.puzzle.height)
            if solution.cells[x][y] == r.UNKNOWN]
