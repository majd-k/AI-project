import time
from typing import List, Dict

class NQueensForwardChecking:
    """
    N-Queens using Backtracking + Forward Checking + MRV
    """

    def __init__(self, n: int):
        self.n = n
        self.solutions = []
        self.nodes_explored = 0
        self.consistency_checks = 0

    def is_consistent(self, row, col, assignment):
        """Check if placing queen at (row, col) is valid with current assignment."""
        for r, c in assignment.items():
            self.consistency_checks += 1

            if c == col:
                return False  # same column
            
            if abs(c - col) == abs(r - row):
                return False  # same diagonal

        return True

    def forward_check(self, row, col, domains):
        """
        Reduce domains of remaining rows after assigning (row, col).
        Return a NEW domain dict if consistent; return None if domain wipeout occurs.
        """
        new_domains = {r: domains[r][:] for r in domains}  # deep copy

        for r in new_domains:
            if r > row:  # only forward rows
                for c in domains[r]:
                    self.consistency_checks += 1

                    same_column = (c == col)
                    same_diag = (abs(c - col) == abs(r - row))

                    if same_column or same_diag:
                        new_domains[r].remove(c)

                # domain wipeout → no solution along this branch
                if len(new_domains[r]) == 0:
                    return None

        return new_domains

    def select_next_variable(self, domains, assignment):
        """
        MRV (Minimum Remaining Values):
        Choose the row with the smallest domain.
        """
        unassigned = [r for r in range(self.n) if r not in assignment]
        return min(unassigned, key=lambda r: len(domains[r]))

    def backtrack(self, assignment, domains):
        """Recursive backtracking with forward checking and MRV."""
        # All queens placed
        if len(assignment) == self.n:
            self.solutions.append(dict(assignment))
            return

        self.nodes_explored += 1

        # Use MRV to pick next variable (next row)
        row = self.select_next_variable(domains, assignment)

        for col in domains[row]:
            if self.is_consistent(row, col, assignment):
                assignment[row] = col

                # Forward checking
                new_domains = self.forward_check(row, col, domains)
                if new_domains is not None:
                    self.backtrack(assignment, new_domains)

                # Undo
                del assignment[row]

    def solve(self):
        print(f"Solving {self.n}-Queens using Backtracking + Forward Checking")

        start = time.time()

        # create initial full domains
        domains = {r: list(range(self.n)) for r in range(self.n)}

        self.backtrack({}, domains)

        elapsed = time.time() - start

        print("============== RESULTS ==============")
        print(f"Solutions found:       {len(self.solutions)}")
        print(f"Nodes explored:        {self.nodes_explored}")
        print(f"Consistency checks:    {self.consistency_checks}")
        print(f"Running time:          {elapsed:.6f} seconds")

        return self.solutions, elapsed


if __name__ == "__main__":
    print("\n" + "-"*70)
    print("N-QUEENS: Backtracking + Forward Checking")
    print("-"*70)

    test_values = [4,6, 8, 10]   # You can change this

    for n in test_values:
        print(f"\nTesting N = {n}")
        solver = NQueensForwardChecking(n)
        solutions, time_taken = solver.solve()

        # show the first solution if exists
        if solutions:
            print("\nFirst solution:")
            sol = solutions[0]
            for r in range(n):
                row = ""
                for c in range(n):
                    if sol[r] == c:
                        row += " Q "
                    else:
                        row += " . "
                print(row)
        else:
            print("No solution found.")
