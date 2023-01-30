from io import StringIO

test = "0 2 7 0"

# with StringIO(test) as f:
with open("input6.txt") as f:
  banks = [int(n) for n in f.readline().strip().split()]

print(banks)
states = []
cycle_found = False

new_state = " ".join([str(n) for n in banks])
while new_state not in states:
    states.append(new_state)

    # print(banks)
    max_value = max(banks)
    max_pos = banks.index(max_value)

    even_split = max_value // len(banks)
    remainder = max_value % len(banks)

    # print(max_value, max_pos)
    # print(even_split, remainder)
    # print("so the next", remainder, "get", even_split + 1, "while the remaining", len(banks) - remainder, "only get", even_split)

    banks[max_pos] = 0
    # print(banks)
    for n in range(remainder):
        banks[(n + max_pos + 1) % len(banks)] += even_split + 1

    for n in range(len(banks) - remainder):
        banks[(n + len(banks) - remainder + 1) % len(banks)] += even_split

    # print(banks)
    new_state = " ".join([str(n) for n in banks])
    # print(states)

    if not cycle_found and new_state in states:
        print("Part 1:", len(states))
        cycle_found = True
        states.clear()

print("Part 2:", len(states))
