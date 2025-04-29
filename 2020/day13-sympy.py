from functools import reduce
from io import StringIO
from math import ceil, log
from operator import add

import sympy as sp
from sympy.solvers.diophantine import diophantine

test = """939
7,13,x,x,59,x,31,19"""

with StringIO(test) as data:
    # with open("input13.txt") as data:
    wait, buses = data.readlines()
    wait = int(wait)
    buses = list(map(int, buses.replace("x", "-1").split(",")))

upper_wait = 10**ceil(log(wait, 10) * 1.5)
print(wait, buses, upper_wait)

best_next = float("inf")
best_bus = -1
for bus in buses:
    if bus != -1:
        stops = range(0, upper_wait, bus)
        next_stop = next((s for s in stops if s > wait))
        if next_stop < best_next:
            best_next = next_stop
            best_bus = bus

print("Part 1:", (best_next - wait) * best_bus)

t = sp.symbols('t')
total_inc = 0
buses_exp = []
for inc, bus in enumerate(buses):
    if bus == -1:
        continue

    total_inc += inc
    buses_exp.append((bus * sp.symbols(f"bus_{bus}")))

print(buses_exp, total_inc)
final_exp = reduce(add, buses_exp)
final_exp -= t + total_inc
print(final_exp)
solution = diophantine(sp.Eq(final_exp, 0), param=t)
print(solution)
