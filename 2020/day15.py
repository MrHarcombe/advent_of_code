from collections import defaultdict
from io import StringIO
from operator import indexOf

test = """0,3,6"""
actual = """14,8,16,0,1,17"""

numbers = [0] * 2021

with StringIO(actual) as values:
    for line in values:
        for pos, number in enumerate(map(int, line.strip().split(","))):
            numbers[pos] = number

for n in range(pos+1, 2021):
    if numbers[n-1] not in numbers[:n-1]:
        numbers[n] = 0

    else:
        numbers[n] = indexOf(reversed(numbers[:n-1]), numbers[n-1]) + 1

    # print(n, "->", numbers[n])

# print(numbers[10])
print(numbers[2019])
