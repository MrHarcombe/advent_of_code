from collections import defaultdict
from io import StringIO

test = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

direction_list = "^>v<"
directions = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}


def get_next_move(floorplan, position, facing):
    x, y = position
    dx, dy = directions[facing]
    next_pos = x + dx, y + dy
    next_dir = facing
    count = 0
    while floorplan.get(next_pos, ".") != ".":
        count += 1
        if count >= 4:
            # print("Bouncing out...")
            raise LookupError()
        next_dir = direction_list[
            (direction_list.index(next_dir) + 1) % len(direction_list)
        ]
        dx, dy = directions[next_dir]
        next_pos = (x + dx, y + dy)

    return next_pos, next_dir


def is_in_range(floorplan, position):
    x, y = position

    return (
        floorplan["MIN_X"] <= x <= floorplan["MAX_X"]
        and floorplan["MIN_Y"] <= y <= floorplan["MAX_Y"]
    )


def display_floorplan(floorplan, visited):
    for y in range(floorplan["MIN_Y"], floorplan["MAX_Y"] + 1):
        row = []
        for x in range(floorplan["MIN_X"], floorplan["MAX_X"] + 1):
            if (x, y) in visited:
                if len(visited[(x, y)]) > 1:
                    row.append("X")
                else:
                    row.append(visited[(x, y)][0])
            else:
                row.append(floorplan.get((x, y), "."))
        print("".join(row))
    print()
    input()


floorplan = {}
start_pos = None
start_dir = None
current_pos = None
current_dir = None
visited = defaultdict(list)

# with StringIO(test) as input_data:
with open("input6.txt") as input_data:
    for y, line in enumerate(input_data):
        for x, ch in enumerate(line.strip()):
            if ch == "^":
                start_pos = (x, y)
                start_dir = ch
            elif ch != ".":
                floorplan[(x, y)] = ch

    min_x = min(x for (x, y) in floorplan)
    max_x = max(x for (x, y) in floorplan)
    min_y = min(y for (x, y) in floorplan)
    max_y = max(y for (x, y) in floorplan)
    floorplan["MIN_X"] = min_x
    floorplan["MAX_X"] = max_x
    floorplan["MIN_Y"] = min_y
    floorplan["MAX_Y"] = max_y

current_pos = start_pos
current_dir = start_dir
visited[current_pos].append(current_dir)

next_pos, next_dir = get_next_move(floorplan, current_pos, current_dir)
while is_in_range(floorplan, next_pos):
    current_pos, current_dir = next_pos, next_dir
    visited[current_pos].append(current_dir)
    next_pos, next_dir = get_next_move(floorplan, current_pos, current_dir)

print("Part 1:", len(visited))

looped = 0
escaped = 0

candidates = set(visited.keys()) - set(start_pos)
# print(candidates)

looped = set()
escaped = set()

for candidate in candidates:
    # print("Trying:", candidate)
    current_pos = start_pos
    current_dir = start_dir
    visited = defaultdict(list)
    visited[current_pos].append(current_dir)

    try:
        # display_floorplan(floorplan | {candidate: "O"}, visited)
        next_pos, next_dir = get_next_move(
            floorplan | {candidate: "#"}, current_pos, current_dir
        )
        while True:
            # display_floorplan(floorplan | {candidate: "O"}, visited)
            if next_dir in visited[next_pos]:
                # print(candidate)
                looped.add(candidate)
                break

            elif not is_in_range(floorplan | {candidate: "#"}, next_pos):
                escaped.add(candidate)
                break

            current_pos, current_dir = next_pos, next_dir
            visited[current_pos].append(current_dir)
            next_pos, next_dir = get_next_move(
                floorplan | {candidate: "#"}, current_pos, current_dir
            )
    except LookupError:
        # print("...caught a loop")
        #  looped.add(candidate)
        pass

print("Part 2:", len(looped))

# 1884/1883 - too high
# 1678 wrong :(
