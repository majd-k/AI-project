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



TESTS = [4, 6, 8, 10]

for N in TESTS:
    print("\n==========================")
    print(f"       N = {N}")
    print("==========================")

    # AC-3
    ac = AC3_Solver(N)
    r = ac.solve()
    print(f"AC3+MRV: \n solutions={r['solutions']} \n expansions={r['node_expansions']} \n checks={r['checks']} \n time={r['time']:.4f}s")

