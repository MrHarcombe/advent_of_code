from dataclasses import dataclass

# cups = "389125467"
cups = "135468729"

@dataclass
class cup:
    value: int
    next_value: int

def move_cups(cups_list: list[cup], current: cup, min_cup: int, max_cup: int):
    # remove the 3 cups after the current
    substart_cup = cups_list[current.next_value]
    current.next_value = cups_list[cups_list[cups_list[substart_cup.next_value].next_value].next_value].value
    sub_values = [substart_cup.value, cups_list[substart_cup.next_value].value, cups_list[cups_list[substart_cup.next_value].next_value].value]

    # check the destination cup is valid
    destination_value = current.value - 1
    while destination_value in sub_values:
        if destination_value < min_cup:
            destination_value = max_cup
        destination_value -= 1

    if destination_value < min_cup:
        destination_value = max_cup

    # transplant the substrand after the destination
    pickup_value = cups_list[destination_value].next_value
    cups_list[destination_value].next_value = substart_cup.value
    cups_list[cups_list[substart_cup.next_value].next_value].next_value = pickup_value

    return cups_list[current.next_value]

def p1_score_cups(cups_list: list[cup]):
    runner_cup = cups_list[cups_list[1].next_value]

    score = 0
    while runner_cup.value != 1:
        score = score * 10 + runner_cup.value
        runner_cup = cups_list[runner_cup.next_value]

    return score

def part1(cups_input: list[int]):
    cups_values = list(map(int, list(cups_input)))
    min_cup = min(cups_values)
    max_cup = max(cups_values)

    # just allocate them all, for accessibility
    cups_list = [cup(n, n+1) for n in range(len(cups_input)+1)]

    for index in range(0, len(cups_values)-1):
        cups_list[cups_values[index]].next_value = cups_values[index+1]

    cups_list[cups_values[-1]].next_value = cups_list[cups_values[0]].value
    current = cups_list[cups_values[0]]

    for _ in range(100):
        current = move_cups(cups_list, current, min_cup, max_cup)

    return p1_score_cups(cups_list)

def part2(cups_input: list[int]):
    cups_values = list(map(int, list(cups_input)))
    min_cup = min(cups_values)
    max_cup = max(cups_values)

    # just allocate them all, for accessibility
    cups_list = [cup(n, n+1) for n in range(1_000_000+1)]

    # only override the cups_input values
    for index in range(0, len(cups_values)-1):
        cups_list[cups_values[index]].next_value = cups_values[index+1]

    # tidy up the unnecessary cups
    for n in range(0, min_cup):
        cups_list[n] = None

    # link back to the beginning
    cups_list[-1].next_value = cups_list[cups_values[0]].value
    current = cups_list[cups_values[0]]

    # print("Added extra cups")

    for n in range(10_000_000):
        current = move_cups(cups_list, current, min_cup, 1_000_000)
        # if n % 1_000_000 == 0:
        #     print("Moved", n, "cups")

    return cups_list[1].next_value * cups_list[cups_list[1].next_value].next_value

print("Part 1:", part1(cups))
print("Part 2:", part2(cups))
