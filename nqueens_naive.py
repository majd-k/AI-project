import time
from typing import List

class NQueensNaive:
    """
    Naive Brute Force Approach to N-Queens Problem
    
    Algorithm:
    1. Generate ALL possible placements (N^N combinations)
    2. For each complete configuration, check if it's valid
    3. A configuration is valid if no two queens attack each other
    
    Time Complexity: O(N^N) - Exponential and very slow
    Space Complexity: O(N)
    """
    
    def __init__(self, n: int):
        self.n = n
        self.solutions = []
        self.nodes_explored = 0  # total configurations checked
        self.consistency_checks = 0  # total constraint checks performed
    
    def is_valid_solution(self, board: List[int]) -> bool:
        """
        Check if a complete board configuration is valid.
        
            board: List where board[i] = column position of queen in row i
            
        Returns:
            True if no two queens attack each other, False otherwise
        """
        # check all pairs of queens
        for i in range(self.n):
            for j in range(i + 1, self.n):
                self.consistency_checks += 1
                
                # check if queens are in same column
                if board[i] == board[j]:
                    return False
                
                # check if queens are on same diagonal
                # two queens at (i, board[i]) and (j, board[j]) are on same diagonal if:
                # |row_diff| == |col_diff|
                if abs(board[i] - board[j]) == abs(i - j):
                    return False
        
        return True
    
    def generate_all_configurations(self, position: int, current_board: List[int]):
        """
        Recursively generate all possible N^N configurations.
        
        Args:
            position: Current row being filled (0 to N-1)
            current_board: Current partial configuration
        """
        # base case: we've placed a queen in every row
        if position == self.n:
            self.nodes_explored += 1
            
            # check if this complete configuration is valid
            if self.is_valid_solution(current_board):
                # found a valid solution
                self.solutions.append(current_board[:])  # make a copy
            return
        
        # try placing queen in each column for current row
        for col in range(self.n):
            current_board[position] = col
            # recursively fill remaining rows
            self.generate_all_configurations(position + 1, current_board)
    
    def solve(self):
        """
        Main solving function - starts the brute force search
        """
        print("-"*70)
        print(f"NAIVE BRUTE FORCE APPROACH - {self.n}-Queens Problem")
        print("-"*70)
        print(f"\nThis will generate and check ALL {self.n}^{self.n} = {self.n**self.n:,} possible configurations!")
        print("Please wait...\n")
        
        start_time = time.time()
        
        # start recursive generation from row 0
        initial_board = [-1] * self.n  # -1 means no queen placed yet
        self.generate_all_configurations(0, initial_board)
        
        elapsed_time = time.time() - start_time
        
        # print results
        print("-"*70)
        print("RESULTS")
        print("-"*70)
        print(f"Board Size (N):              {self.n}")
        print(f"Total Configurations:        {self.n**self.n:,}")
        print(f"Configurations Checked:      {self.nodes_explored:,}")
        print(f"Consistency Checks:          {self.consistency_checks:,}")
        print(f"Valid Solutions Found:       {len(self.solutions)}")
        print(f"Time Elapsed:                {elapsed_time:.6f} seconds")
        
        if elapsed_time > 0:
            configs_per_sec = self.nodes_explored / elapsed_time
            print(f"Configurations/Second:       {configs_per_sec:,.0f}")
        
        return self.solutions, elapsed_time
    
    def print_board(self, board: List[int]):
        """
        Print a chessboard configuration in a visual format.
        
        Args:
            board: List where board[i] = column of queen in row i
        """
        print()
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if board[row] == col:
                    line += " Q "
                else:
                    line += " . "
            print(line)
        print()
    
    def display_solutions(self, max_display: int = 3):
        if not self.solutions:
            print("\nNo solutions found!")
            return
        
        print("\n" + "-"*70)
        print(f"DISPLAYING SOLUTIONS (showing up to {max_display} of {len(self.solutions)})")
        print("="*70)
        
        for i, solution in enumerate(self.solutions[:max_display]):
            print(f"\nSolution #{i + 1}:")
            self.print_board(solution)
        
        if len(self.solutions) > max_display:
            print(f"... and {len(self.solutions) - max_display} more solutions")


if __name__ == "__main__":
    print("\n" + "-"*70)
    print("N-QUEENS PROBLEM: NAIVE BRUTE FORCE APPROACH")
    print("-"*70)
    print("\nThis approach tries EVERY possible configuration!")
    print("It's simple but extremely inefficient.\n")
    
    # test with different N values
    test_cases = [4,6,8,10]  # be careful with N > 8, it'll be very slow
    
    for n in test_cases:
        print(f"\n{'-'*70}")
        print(f"Testing with N = {n}")
        print(f"{'-'*70}")
        
        # warn user for large N
        if n > 8:
            print(f"N={n} will generate {n**n:,} configurations!")
            print("This might take a very long time!")
            response = input("Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("Skipped.")
                continue
        
        solver = NQueensNaive(n)
        solutions, time_taken = solver.solve()
        solver.display_solutions(max_display=2)
        
        # analysis
        print("\n" + "-"*70)
        print("ANALYSIS")
        print("-"*70)
        print(f"Efficiency: Checked {solver.nodes_explored:,} configurations")
        print(f"            Found {len(solutions)} solutions")
        if len(solutions) > 0:
            success_rate = (len(solutions) / solver.nodes_explored) * 100
            print(f"            Success Rate: {success_rate:.4f}%")
            print(f"            That's only 1 in {solver.nodes_explored // len(solutions):,} configurations!")
        
        print("\n" + "-"*70)