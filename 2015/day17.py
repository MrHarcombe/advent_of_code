test = '''20
15
10
5
5'''

def subset_sum(numbers, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        remaining = numbers[i + 1:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)

target = 150 # 25 for test, 150 for live

import io
# with io.StringIO(test) as inputs:
with open('input17.txt') as inputs:
    containers = [int(n) for n in inputs.readlines()]

    solutions = list(subset_sum(containers, target))
    minimum = min([len(s) for s in solutions])
    print(len([s for s in solutions if len(s) == minimum]))
