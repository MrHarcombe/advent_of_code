from collections import defaultdict
from io import StringIO

test = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

def get_time_taken(step):
    return ord(step) - ord("A") + 61

def get_next_available(steps):
    try:
        return next(iter(sorted([step for step, pre in steps.items() if len(pre) == 0])))
    except:
        return None

def remove_from_steps(step, steps):
    if step in steps:
        del steps[step]
    for affected in [s for s in steps if step in steps[s]]:
        steps[affected].remove(step)

steps = defaultdict(lambda: [])

# with StringIO(test) as data:
with open("input7.txt") as data:
    for line in data:
        parts = line.strip().split()
        pre, step = parts[1], parts[7]

        steps[pre]
        steps[step].append(pre)
        steps[step].sort()

def part1():
    step = get_next_available(steps)
    remove_from_steps(step, steps)
    order = [step]

    while len(steps) > 0:
        step = get_next_available(steps)
        remove_from_steps(step, steps)
        order.append(step)

    print("Part 1:", "".join(order))

def part2():
    time = -1
    elves = 5
    working = {}
    order = []
    while len(steps) > 0 or len(working) > 0:
        time += 1
        for elf in range(elves):
            if elf in working:
                step, due = working[elf]
                due -= 1
                if due <= 0:
                    remove_from_steps(step, steps)
                    order.append(step)
                    del working[elf]
                else:
                    working[elf] = (step, due)
            
            if elf not in working:
                step = get_next_available(steps)
                if step is not None:
                    del steps[step]
                    working[elf] = (step, get_time_taken(step))
        # print(time, order, working)

    print("Part 2:", time, "".join(order))

# part1()
part2()