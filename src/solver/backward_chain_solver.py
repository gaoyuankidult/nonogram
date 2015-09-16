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

import rules.nonogram as rules

# TODO ggould figure out why pycharm dislikes doing these as local imports.
from solver.solver_utils import all_legal_lines
from solver.solver_coroutine import SolverCoroutine, SolutionNotFound


class BackwardChainSolver(SolverCoroutine):
    """A solver (see solver_coroutine.py for API details) that uses
    alternating deductive and recursive phases."""

    def __init__(self, puzzle, initial_solution=None):
        super(BackwardChainSolver, self).__init__(puzzle, initial_solution)
        self.partial_solution = None
        self.partial_solution_legal_rows = None
        self.partial_solution_legal_cols = None
        self.update_partials(self.initial_solution.clone())

    def update_partials(self, new_partial):
        """Update the solver with a new partial solution, and causes
        regeneration of the cached legal rows/columns."""
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
            possible_lines = self.partial_solution_legal_cols[x]
            for y in range(self.puzzle.height):
                if new_partial_solution.cells[x][y] != rules.UNKNOWN:
                    continue
                if len(set(line[y] for line in possible_lines)) == 1:
                    changed = True
                    new_partial_solution.cells[x][y] = possible_lines[0][y]
        for (y, row) in enumerate(self.partial_solution.rows):
            possible_lines = self.partial_solution_legal_rows[y]
            for x in range(self.puzzle.width):
                if new_partial_solution.cells[x][y] != rules.UNKNOWN:
                    continue
                if len(set(line[x] for line in possible_lines)) == 1:
                    changed = True
                    new_partial_solution.cells[x][y] = possible_lines[0][x]
        if changed:
            self.update_partials(new_partial_solution)
        return changed

    def solve(self):
        """Yield a partial solution from each iteration of deduction, then
        delegate to the solve() coroutines of hypotheses on a chosen cell.

        Returns after a complete solution or after it proves that the
        initial_solution is impossible."""
        yield self.initial_solution
        # Iterate deduction to fixity.
        while self.deduce():
            if not self.partial_solution.correct():
                raise SolutionNotFound("Deduction forced a contradiction")
            if any(len(rows) == 0
                   for rows in self.partial_solution_legal_rows):
                # Deduction created an impossible row.
                raise SolutionNotFound("Deduction created an impossible row")
            if any(len(cols) == 0
                   for cols in self.partial_solution_legal_cols):
                # Deduction created an impossible column.
                raise SolutionNotFound(
                    "Deduction created an impossible column")
            yield self.partial_solution

        # Identify a cell to hypothesize about.
        unknowns = self.partial_solution.unknown_cell_coordinates()
        if not unknowns:
            # Deduction produced a complete solution; we win.
            return

        # Sort unknowns to prefer cases where hypotheses are likely to
        # generate cascading inferences.
        _, speculation_coords = min(
            ((len(self.partial_solution_legal_rows[y]) +
              len(self.partial_solution_legal_cols[x])),
             (x, y))
            for (x, y) in unknowns)

        # Hypothesize a cell value; delegate to a new solver for that
        # hypothesis.
        hypothetical_solvers = []
        # TODO ggould Trying unmarking first on the hunch that unmarks can
        # sometimes get big splitting leverage.  This is a half-baked idea;
        # needs any theoretical or even empirical justification.
        for fn in (rules.NonogramSolution.unmark,
                   rules.NonogramSolution.mark):
            solver = BackwardChainSolver(
                self.puzzle, initial_solution=self.partial_solution.clone())
            partial = solver.partial_solution.clone()
            fn(partial, speculation_coords)
            solver.update_partials(partial)
            hypothetical_solvers.append(solver)
        # TODO ggould Can we sort these solvers sensibly?
        # TODO ggould Is there a way around Global Interpreter Locking to
        # get multicore leverage on this?
        for solver in hypothetical_solvers:
            try:
                yield from solver.solve()
                # Victory!  This hypothesis found a correct solution.
                return
            except SolutionNotFound as _:
                pass  # Ignore this and move on to the next.
        raise SolutionNotFound("All hypotheses at %s failed",
                               speculation_coords)
