from io import StringIO
from time import time
import numpy as np

# Part 1
MAX_DEPTH = 25
# Part 2
# MAX_DEPTH = 33

def get_neighbours(state, blueprints):
    options = []

    for robot in ("geode", "obsidian", "clay", "ore"):
        if robot == "ore" and state[4] >= blueprints["max_ore"]:
            # print("enough ore robots", state[4])
            continue
        elif robot == "clay" and state[5] >= blueprints["max_clay"]:
            # print("enough clay robots", state[5])
            continue
        elif robot == "obsidian" and state[6] >= blueprints["max_obsidian"]:
            print("enough obsidian robots", state[6])
            continue

        build_state = state.copy()
        affordable = True

        for amount, item in blueprints[robot]:
            if item == "ore" and amount <= build_state[0]:
                build_state[0] -= amount
            elif item == "clay" and amount <= build_state[1]:
                build_state[1] -= amount
            elif item == "obsidian" and amount <= build_state[2]:
                build_state[2] -= amount
            else:
                affordable = False
                break

        if affordable:
            if robot == "ore": robot_index = 4
            elif robot == "clay": robot_index = 5
            elif robot == "obsidian": robot_index = 6
            elif robot == "geode": robot_index = 7
            else: print("*** unknown robot ***")

            build_state[robot_index] += 1
            build_state[0] += state[4]
            build_state[1] += state[5]
            build_state[2] += state[6]
            build_state[3] += state[7]
            options.append((f"build-{robot}", build_state))

            if robot == "geode" or (robot == "obsidian" and build_state[robot_index] == 1):
                return options

    if sum(state[4:]) > 0:
        use_state = state.copy()
        use_state[0] += state[4]
        use_state[1] += state[5]
        use_state[2] += state[6]
        use_state[3] += state[7]
        options.append(("use", use_state))

    return options

def depth_first(start_node, start_state, blueprints):
    stack = []

    stack.append(([start_node],start_state))
    while len(stack) > 0:
        # if len(stack) % 10000 == 0:
        #     print("stack size:", len(stack))
        current_path, current_state = stack.pop()
        # print(len(current_path), current_state)

        if len(current_path) >= MAX_DEPTH:
            yield current_path, current_state

        else:
            for next_turn, next_state in get_neighbours(current_state, blueprints):
                next_path = list(current_path) + [next_turn]

                if len(next_path) <= MAX_DEPTH:
                    stack.append((next_path, next_state))
                else:
                    print("ignoring: too long")


def breadth_first(start_node, start_state, blueprints):
    queue = []

    queue.append(([start_node],start_state))
    while len(queue) > 0:
        current_path, current_state = queue.pop(0)
        # print(len(current_path), current_state)

        if len(current_path) >= MAX_DEPTH:
            yield current_path, current_state

        else:
            for next_turn, next_state in get_neighbours(current_state, blueprints):
                next_path = list(current_path) + [next_turn]

                if len(next_path) <= MAX_DEPTH:
                    queue.append((next_path, next_state))
                else:
                    print("ignoring: too long")

test = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

blueprints = {}

with StringIO(test) as f:
# with open("input19.txt") as f:
    for line in f:
        number, content = line.strip().split(":")
        number = int(number.split(" ")[1])
        blueprints[number] = {}
        robots = content.split(".")[:-1]

        # print(number, robots[:-1])
        for robot in robots:
            name, costs = robot.split("costs")
            name = name.split()[1]
            costs = tuple(tuple(int(bit) if n == 0 else bit for n, bit in enumerate(part.strip().split())) for part in costs.split("and"))
            # print(name, costs)
            
            blueprints[number][name] = costs

        max_ore = 0
        max_clay = 0
        max_obsidian = 0
        for robot in blueprints[number]:
            for amount, item in blueprints[number][robot]:
                if item == "ore": max_ore = max(max_ore, amount)
                elif item == "clay": max_clay = max(max_clay, amount)
                elif item == "obsidian": max_obsidian = max(max_obsidian, amount)
                else: print("*** unknown component ***")

        blueprints[number]["max_ore"] = max_ore
        blueprints[number]["max_clay"] = max_clay
        blueprints[number]["max_obsidian"] = max_obsidian

# options:
# - use robot (1 minute, gain 1 resource)
# - build robot (1 minute, gain 1, cost from blueprint)

# state holds:
# - ore
# - clay
# - obsidian
# - geodes
# - ore robots
# - clay robots
# - obsidian robots
# - geode robots

start = time()

initial_node = "start"
initial_state = np.array([0,0,0,0,1,0,0,0])

# option_count = 0
# max_geodes = 0
# onefor option in depth_first(initial_node, initial_state, blueprints[1]):
#     if "build-geode" in option[0]:
#         if option[1][3] > max_geodes:
#             print(option)
#         max_geodes = max(max_geodes, option[1][3])
#         # if option_count % 1000 == 0:
#         #     option_count += 1
#         # print("geodes:", option[1])
# 
# print(max_geodes)

# total_1 = 0
total_2 = 1
for blueprint in blueprints:
    print("Blueprint:", blueprint)
    # print(max(breadth_first(initial_node, initial_state, blueprints[blueprint]), key=lambda i:i[1][-1]))

    max_geodes = 0
    for option in depth_first(initial_node, initial_state, blueprints[blueprint]):
        if "build-geode" in option[0]:
            if option[1][3] > max_geodes:
                print(option[1], ", ".join(option[0][1:]))
            max_geodes = max(max_geodes, option[1][3])
            # total_1 += blueprint * max_geodes[1][3]
    total_2 *= max_geodes

    # max_geodes = max(depth_first(initial_node, initial_state, blueprints[blueprint]), key=lambda option: option[1][3])
    # print(blueprint, "->", max_geodes[1][3], max_geodes[0])
    # # total_1 += blueprint * max_geodes[1][3]
    # total_2 *= max_geodes[1][3]

print("Total:", total_2)
print("Time:", time() - start)
