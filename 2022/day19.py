from io import StringIO
from time import time

# Part 1
# MAX_DEPTH = 24
# Part 2
MAX_DEPTH = 32

# def score_state(state):
#     return state[0] + state[1] * 10 + state[2] * 100 + state[3] * 1000 + state[4] * 10000 + state[5] * 100000 + state[6] * 1000000 + state[7] * 10000000

def triangular(side):
    return (1 + side) * side // 2

def get_neighbours(state, previous, blueprints, cache, current_depth, current_max):
    # could we beat the current best?
    if triangular(MAX_DEPTH - current_depth) <= current_max - state[3] - state[7]:
        # print(f"can't beat best {current_max} at depth {current_depth}")
        return []

    # have we been "here" before
    if state in cache:
        return cache[state]

    options = []

    for robot in (7, 6, 5, 4):
        if robot < 7 and current_depth >= MAX_DEPTH - 2 or \
           robot == 7 and current_depth >= MAX_DEPTH - 1 or \
           state[robot] >= blueprints["max"][robot]:
            continue

        if blueprints[robot][0] <= state[0] and blueprints[robot][1] <= state[1] and blueprints[robot][2] <= state[2]:
            # if you find that you could've afforded this robot last turn, but waited, then prune this branch
            if blueprints[robot][0] <= previous[0] and blueprints[robot][1] <= previous[1] and blueprints[robot][2] <= previous[2] \
               and state[4] == previous[4] and state[5] == previous[5] and state[6] == previous[6] and state[7] == previous[7]:
                continue

            build_state = list(state)

            build_state[0] -= blueprints[robot][0]
            build_state[1] -= blueprints[robot][1]
            build_state[2] -= blueprints[robot][2]
            build_state[robot] += 1

            build_state[0] += state[4]
            build_state[1] += state[5]
            build_state[2] += state[6]
            build_state[3] += state[7]

            options.append(build_state)

            # if robot == 7 or (robot == 6 and build_state[robot] == 1):
            if robot == 7:
                cache[state] = options
                return options

    if sum(state[4:]) > 0:
        use_state = list(state)
        use_state[0] += state[4]
        use_state[1] += state[5]
        use_state[2] += state[6]
        use_state[3] += state[7]
        options.append(use_state)

    cache[state] = options
    return options

# def reduce_stack(stack, depth, ore_bots, clay_bots, obsidian_bots, geode_bots):
#     # print("Reducing:", depth, ore_bots, clay_bots, obsidian_bots, geode_bots)
#     def include_state(item):
#         idepth, istate, imax = item
#         return idepth != depth or idepth == depth and istate[4] > ore_bots and istate[5] > clay_bots and istate[6] > obsidian_bots and istate[7] > geode_bots
# 
#     return filter(include_state, stack)

def depth_first(start_state, blueprints, cache):
    stack = [(0, start_state, start_state, 0)]
    visited = set()

    while len(stack) > 0:
        current_depth, current_state, previous_state, current_max = stack.pop()
        visited.add((current_depth, current_state))

        if current_depth >= MAX_DEPTH:
            yield current_state

        else:
            for next_state in get_neighbours(current_state, previous_state, blueprints, cache, current_depth, current_max):
                current_max = max(current_max, next_state[7])
                # stack = list(reduce_stack(stack, current_depth+1, *next_state[4:]))
                if current_depth + 1 <= MAX_DEPTH and (current_depth + 1, tuple(next_state)) not in visited:
                    stack.append((current_depth + 1, tuple(next_state), current_state, current_max))

    # print(current_state)
    yield current_state

# def breadth_first(start_state, blueprints, cache):
#     queue = [(0, start_state, 0)]
#     visited = set()
# 
#     while len(queue) > 0:
#         current_depth, current_state, current_max = queue.pop(0)
#         visited.add((current_depth, current_state))
#         # print(len(current_path), current_state)
# 
#         if current_depth >= MAX_DEPTH:
#             return current_state
# 
#         else:
#             for next_state in get_neighbours(current_state, blueprints, cache, current_depth, current_max):
#                 current_max = max(current_max, next_state[7])
#                 if current_depth + 1 <= MAX_DEPTH and (current_depth+1, tuple(current_state)) not in visited:
#                     queue.append((current_depth + 1, tuple(next_state), current_max))

test = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

blueprints = {}

# with StringIO(test) as f:
with open("input19.txt") as f:
    for line in f:
        number, content = line.strip().split(":")
        number = int(number.split(" ")[1])
        blueprints[number] = {}
        robots = content.split(".")[:-1]

        # print(number, robots[:-1])
        for robot in robots:
            name, costs = robot.split("costs")
            name = name.split()[1]
            if name == "ore":
                name_index = 4
            elif name == "clay":
                name_index = 5
            elif name == "obsidian":
                name_index = 6
            elif name == "geode":
                name_index = 7
            
            parsed_costs = tuple(tuple(int(bit) if n == 0 else bit for n, bit in enumerate(part.strip().split())) for part in costs.split("and"))
            costs = [0,0,0]
            for cost, material in parsed_costs:
                if material == "ore":
                    costs[0] = cost
                elif material == "clay":
                    costs[1] = cost
                elif material == "obsidian":
                    costs[2] = cost
            # print(name, costs)

            blueprints[number][name_index] = costs

        blueprints[number]["max"] = {}
        blueprints[number]["max"][4] = 0
        blueprints[number]["max"][5] = 0
        blueprints[number]["max"][6] = 0
        blueprints[number]["max"][7] = float("inf")

        for robot in (4,5,6,7):
            costs = blueprints[number][robot]
            blueprints[number]["max"][4] = max(blueprints[number]["max"][4], costs[0])
            blueprints[number]["max"][5] = max(blueprints[number]["max"][5], costs[1])
            blueprints[number]["max"][6] = max(blueprints[number]["max"][6], costs[2])

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
initial_depth = 0
initial_state = (0,0,0,0,1,0,0,0)

# total_1 = 0
total_2 = 1
# for blueprint in blueprints:
for blueprint in range(1, 4):
    # print("Blueprint:", blueprint)

    # max_geodes = 0
    # for option in depth_first(initial_depth, initial_state, blueprints[blueprint]):
    #     if option[1][3] > max_geodes:
    #         print(option[1], option[0])
    #     max_geodes = max(max_geodes, option[1][3])
    #     total_1 += blueprint * max_geodes[1][3]
    # # total_2 *= max_geodes

    max_geodes = max(depth_first(initial_state, blueprints[blueprint], {}), key=lambda option: option[3])
    # max_geodes = breadth_first(initial_state, blueprints[blueprint], {})
    print(blueprint, "->", max_geodes, blueprint * max_geodes[3])
    # total_1 += blueprint * max_geodes[3]
    total_2 *= max_geodes[3]

print("Total:", total_2)
print("Time:", time() - start)
