from io import StringIO
from time import time

test = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def is_possible(target, operands, part2=False):
    previous_inputs = [operands.pop(0)]
    while len(operands) > 0:
        next_operand = operands.pop(0)
        next_inputs = []
        for value in previous_inputs:
            next_value = value + next_operand
            if next_value <= target:
                next_inputs.append(next_value)
            next_value = value * next_operand
            if next_value <= target:
                next_inputs.append(next_value)
            if part2:
                next_value = int(str(value) + str(next_operand))
                if next_value <= target:
                    next_inputs.append(next_value)
        previous_inputs = next_inputs

    for total in next_inputs:
        if total == target:
            return total
    return 0


possibles1 = 0
possibles2 = 0

begin = time()

# with StringIO(test) as input_data:
with open("input7.txt") as input_data:
    for line in input_data:
        target, rest = line.strip().split(":")
        target = int(target)
        operands = list(map(int, rest.split()))

        # print(target, operands)

        possibles1 += is_possible(target, list(operands))
        possibles2 += is_possible(target, list(operands), part2=True)

print("Part 1:", possibles1)
print("Part 2:", possibles2)
print("Elapsed:", time() - begin)
