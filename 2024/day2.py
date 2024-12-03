from io import StringIO
from itertools import pairwise

test = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

def get_checks(levels):
     return [a > b for (a,b) in levels], [a < b for (a,b) in levels], [abs(a-b) < 4 for (a,b) in levels]

safe1 = 0
safe2 = 0
# with StringIO(test) as level_data:
with open("input2.txt") as level_data:
    for line in level_data:
            raw_line = line.strip().split()
            levels = list(pairwise(map(int, raw_line)))
            inc, dec, tol = get_checks(levels)
            all_inc = all(inc)
            all_dec = all(dec)
            all_tol = all(tol)

            if (all_inc or all_dec) and all_tol:
                safe1 += 1
                safe2 += 1

            else:
                 for i in range(len(raw_line)):
                      dampener_levels = list(pairwise(map(int, raw_line[:i] + raw_line[i+1:])))
                      dampener_inc, dampener_dec, dampener_tol = get_checks(dampener_levels)
                      if (all(dampener_inc) or all(dampener_dec)) and all(dampener_tol):
                        safe2 += 1
                        break

print("Part 1:", safe1)
print("Part 2:", safe2)