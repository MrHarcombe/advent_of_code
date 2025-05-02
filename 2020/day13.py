from functools import reduce
from io import StringIO
from math import ceil, log, prod
from operator import add

test = """939
7,13,x,x,59,x,31,19"""

# test = """1
# 17,x,13,19"""

# test = """1
# 67,7,59,61"""

# test = """1
# 67,x,7,59,61"""

# test = """1
# 67,7,x,59,61"""

# test = """1
# 1789,37,47,1889"""

###
#
# A Python3 program to demonstrate working of Chinise remainder Theorem
# from https://www.geeksforgeeks.org/introduction-to-chinese-remainder-theorem/

# Returns the smallest number x such that:
# x % num[0] = rem[0],
# x % num[1] = rem[1],
# ..................
# x % num[k-2] = rem[k-1]
#
# Assumption: Numbers in num[] are pairwise coprime (gcd for every pair is 1)


def slow_find_minimum_x(num, rem):
    x = 1  # Initialize result
    k = len(num)

    # As per the Chinese remainder theorem, this loop will always break.
    while True:

        # Check if remainder of x % num[j] is rem[j] or not
        # (for all j from 0 to k-1)
        j = 0
        while (j < k):
            if (x % num[j] != rem[j]):
                break
            j += 1

        # If all remainders matched, we found x
        if (j == k):
            return x

        # Else try next number
        x += 1


###
#
# Optimised CRT solution (using an extended Euclidean algorithm)
# from https://www.geeksforgeeks.org/chinese-remainder-theorem-in-python/


def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x, y = y1 - (b // a) * x1, x1
    return gcd, x, y


def find_minimum_x(num, rem):
    prod_num = prod(num)

    result = 0
    for i in range(len(num)):
        prod_i = prod_num // num[i]
        _, inv_i, _ = gcd_extended(prod_i, num[i])
        result += rem[i] * prod_i * inv_i

    return result % prod_num


# with StringIO(test) as data:
with open("input13.txt") as data:
    wait, buses = data.readlines()
    wait = int(wait)
    buses = list(map(int, buses.replace("x", "-1").split(",")))

# upper_wait = 10**ceil(log(wait, 10) * 1.5)
# print(wait, buses, upper_wait)

# best_next = float("inf")
# best_bus = -1
# for bus in buses:
#     if bus != -1:
#         stops = range(0, upper_wait, bus)
#         next_stop = next((s for s in stops if s > wait))
#         if next_stop < best_next:
#             best_next = next_stop
#             best_bus = bus

# print("Part 1:", (best_next - wait) * best_bus)

bus_numbers = []
bus_offsets = []
for inc, bus in enumerate(buses):
    if bus == -1:
        continue

    bus_numbers.append(bus)
    bus_offsets.append(0 if inc == 0 else bus - inc)

print(bus_numbers, bus_offsets)
print(find_minimum_x(bus_numbers, bus_offsets))
