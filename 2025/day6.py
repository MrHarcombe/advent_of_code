from io import StringIO
from math import prod

test = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

def part1(homework):
    operations = homework.pop()
    total = 0

    while len(homework[0]):
        task = [int(h.pop(0)) for h in homework]
        
        if operations.pop(0) == "+":
            total += sum(task)
        else:
            total += prod(task)

    return total

def part2(homework):
    total = 0

    while len(homework[0]):
        numbers = []
        found_operator = False
        while not found_operator:
            number = [h.pop() for h in homework]
            if all([n == " " for n in number]):
                continue
            numbers.append(int("".join(number[:-1])))
            if number[-1] in ("+", "*"):
                found_operator = True
            
        if number[-1] == "+":
            total += sum(numbers)
        else:
            total += prod(numbers)

    return total

homework = []
# with StringIO(test) as file:
with open("input6.txt") as file:
    for line in file:
        homework.append(line.strip("\n"))

print("Part 1:", part1([h.split() for h in homework]))
print("Part 2:", part2([list(h) for h in homework]))
