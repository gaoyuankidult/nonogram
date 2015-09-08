"""A solver that alternates between deductive and hypothetical phases:

Deductive phase:
 * Generate a list of all possible lines for each row and column.
 * For each list, mark or unmark any cell that is in common between all of
   the possible lines.
 * Iterate to fixity.

Hypothetical phase:
 * Find the cell with the fewest possible row and possible column lines.
 * Explore each possible value in turn.
"""

import rules.nonogram as r

from solver_utils import unknown_cell_coordinates, all_legal_lines
from solver_coroutine import SolverCoroutine


class BackwardChainSolver(SolverCoroutine):
    def __init__(self, puzzle, initial_solution=None):
        self.puzzle = puzzle
        self.initial_solution = initial_solution or r.NonogramSolution(puzzle)
        self.update_partials(self.initial_solution)


    def update_partials(self, new_partial):
        self.partial_solution = new_partial
        self.partial_solution_legal_rows = [
            list(all_legal_lines(self.puzzle.row_run_counts[y],
                                 self.partial_solution.row(y)))
            for y in range(self.puzzle.height)]
        self.partial_solution_legal_cols = [
            list(all_legal_lines(self.puzzle.col_run_counts[x],
                                 self.partial_solution.column(x)))
            for x in range(self.puzzle.width)]


    def deduce(self):
        """Change UNKNOWN cells to MARKED or UNMARKED in self.partial_solution
        where that can be inferred from commonalities between the possible
        lines.  Return True if changes were made, to allow the caller to
        iterate this method to fixity."""
        new_partial_solution = self.partial_solution.clone()
        changed = False
        for (x, col) in enumerate(self.partial_solution.columns):
            col_runs = self.puzzle.col_run_counts[x]
            possible_lines = self.partial_solution_legal_cols[x]
            for y in range(self.puzzle.height):
                if new_partial_solution.cells[x][y] != r.UNKNOWN: continue
                if len(set(line[y] for line in possible_lines)) == 1:
                    changed = True
                    new_partial_solution.cells[x][y] = possible_lines[0][y]
        for (y, row) in enumerate(self.partial_solution.rows):
            row_runs = self.puzzle.row_run_counts[y]
            possible_lines = self.partial_solution_legal_rows[y]
            for x in range(self.puzzle.width):
                if new_partial_solution.cells[x][y] != r.UNKNOWN: continue
                if len(set(line[x] for line in possible_lines)) == 1:
                    changed = True
                    new_partial_solution.cells[x][y] = possible_lines[0][x]
        if changed:
            self.update_partials(new_partial_solution)
        return changed

    def solve(self):
        yield self.initial_solution
        # Iterate deduction to fixity.
        while self.deduce():
            yield self.partial_solution
        # Identify a cell to hypothesize about.
        unknowns = unknown_cell_coordinates(self.partial_solution)
        if not unknowns:
            return
        _, speculation_coords = min((len(self.partial_solution_legal_rows[y]) +
                                     len(self.partial_solution_legal_cols[x]),
                                     (x,y))
                                    for (x,y) in unknowns)
        # Hypothesize a cell value; delegate to a new solver for that
        # hypothesis.
        for fn in (r.NonogramSolution.mark, r.NonogramSolution.unmark):
            solver = BackwardChainSolver(
                self.puzzle, initial_solution=self.partial_solution.clone())
            partial = solver.partial_solution.clone()
            fn(partial, speculation_coords)
            solver.update_partials(partial)
            for child_partial in solver.solve():
                if child_partial is not None:
                    yield child_partial
                    if child_partial.complete():
                        return
