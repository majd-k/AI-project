import time
import itertools
import random
import math
from collections import deque


def revise(domains, xi, xj, N, counter):
    revised = False
    remove_list = []

    for a in domains[xi]:
        ok = False
        for b in domains[xj]:
            counter[0] += 1
            if b != a and abs(a - b) != abs(xi - xj):
                ok = True
                break
        if not ok:
            remove_list.append(a)

    for a in remove_list:
        domains[xi].remove(a)
        revised = True

    return revised

class AC3_Solver:
    def __init__(self, N):
        self.N = N
        self.node_expansions = 0
        self.consistency_checks = 0
        self.solutions = 0

    def initial_domains(self):
        return {r: set(range(self.N)) for r in range(self.N)}

    def MRV(self, domains, assigned):
        unassigned = [v for v in range(self.N) if v not in assigned]
        return min(unassigned, key=lambda x: len(domains[x]))

    def ac3(self, domains):
        queue = deque()
        counter = [0]

        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    queue.append((i, j))

        while queue:
            xi, xj = queue.popleft()
            if revise(domains, xi, xj, self.N, counter):
                if len(domains[xi]) == 0:
                    self.consistency_checks += counter[0]
                    return False
                for xk in range(self.N):
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))

        self.consistency_checks += counter[0]
        return True

    def backtrack(self, domains, assigned):
        if len(assigned) == self.N:
            self.solutions += 1
            return

        var = self.MRV(domains, assigned)

        for val in sorted(domains[var]):
            self.node_expansions += 1
            new_d = {v: set(domains[v]) for v in domains}
            new_d[var] = {val}

            # Remove conflicts
            for other in range(self.N):
                if other == var: continue

                if val in new_d[other]:
                    new_d[other].remove(val)

                d1 = val + (other - var)
                d2 = val - (other - var)
                if 0 <= d1 < self.N and d1 in new_d[other]:
                    new_d[other].remove(d1)
                if 0 <= d2 < self.N and d2 in new_d[other]:
                    new_d[other].remove(d2)

                if len(new_d[other]) == 0:
                    new_d = None
                    break

            if new_d is None:
                continue

            if self.ac3(new_d):
                assigned[var] = val
                self.backtrack(new_d, assigned)
                del assigned[var]

    def solve(self):
        domains = self.initial_domains()
        start = time.perf_counter()
        self.ac3(domains)
        self.backtrack(domains, {})
        elapsed = time.perf_counter() - start
        return {
            "solutions": self.solutions,
            "node_expansions": self.node_expansions,
            "checks": self.consistency_checks,
            "time": elapsed
        }

if __name__ == "__main__":
    print("\n" + "-"*70)
    print("N-QUEENS: Backtracking + AC3")
    print("-"*70)

    test_values = [4, 6, 8, 10]

    for n in test_values:
        print(f"\nTesting N = {n}")
        solver = AC3_Solver(n)
        results = solver.solve()

        print(f"Solutions: {results['solutions']}")
        print(f"Node expansions: {results['node_expansions']}")
        print(f"Checks: {results['checks']}")
        print(f"Time: {results['time']:.6f} sec")

   
        if results["solutions"] > 0:
            print("\nFirst solution:")
            sol = {}
            domains = solver.initial_domains()
            solver.ac3(domains)

            def get_first(dom, assigned):
                if len(assigned) == n:
                    return assigned
                var = solver.MRV(dom, assigned)
                for val in sorted(dom[var]):
                    new_d = {v: set(dom[v]) for v in dom}
                    new_d[var] = {val}
                    ok = True
                    for other in range(n):
                        if other == var: continue
                        if val in new_d[other]:
                            new_d[other].remove(val)
                        d1 = val + (other - var)
                        d2 = val - (other - var)
                        if d1 in new_d[other]:
                            new_d[other].remove(d1)
                        if d2 in new_d[other]:
                            new_d[other].remove(d2)
                        if len(new_d[other]) == 0:
                            ok = False
                            break
                    if not ok: continue
                    if solver.ac3(new_d):
                        assigned[var] = val
                        res = get_first(new_d, assigned)
                        if res: return res
                        del assigned[var]
                return None

            sol = get_first(domains, {})
            board = [sol[r] for r in range(n)]
            for r in range(n):
                print(" ".join("Q" if board[r] == c else "." for c in range(n)))

        else:
            print("No solution found.")
