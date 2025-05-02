from collections import defaultdict
from io import StringIO
from operator import indexOf

test = """0,3,6"""
actual = """14,8,16,0,1,17"""

initial_numbers = []
numbers = defaultdict(lambda: [])

with StringIO(actual) as values:
    for line in values:
        for number in map(int, line.strip().split(",")):
            initial_numbers.append(number)

for n in range(30_000_000 + 1):
    if n < len(initial_numbers):
        number = initial_numbers[n]
        numbers[number].append(n)

    elif len(numbers[number]) < 2:
        number = 0
        numbers[number].append(n)
        if len(numbers[number]) > 2:
            numbers[number].pop(0)

    else:
        number = numbers[number][1] - numbers[number][0]
        numbers[number].append(n)
        if len(numbers[number]) > 2:
            numbers[number].pop(0)

    if n in (2019, 30_000_000 - 1):
        print(n, "->", number)
