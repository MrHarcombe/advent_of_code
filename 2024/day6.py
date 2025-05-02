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
directions = { "^" : (0, -1), ">" : (1, 0), "v" : (0, 1), "<" : (-1, 0) }

def get_next_move(floorplan, position, facing):
    x, y = position
    dx, dy = directions[facing]
    next_pos = x + dx, y + dy
    next_dir = facing
    if floorplan.get(next_pos, ".") == "#":
        next_dir = direction_list[(direction_list.index(facing) + 1) % len(direction_list)]
        dx, dy = directions[next_dir]
        next_pos = (x + dx, y + dy)

    return next_pos, next_dir

def is_in_range(floorplan, position):
    x, y = position
    min_x = min(x for x,y in floorplan)
    max_x = max(x for x,y in floorplan)
    min_y = min(y for x,y in floorplan)
    max_y = max(y for x,y in floorplan)
    
    return min_x <= x <= max_x and min_y <= y <= max_y

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
                start_pos = (x,y)
                start_dir = ch
            elif ch != ".":
                floorplan[(x,y)] = ch

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

min_x = min(x for x,y in visited)
max_x = max(x for x,y in visited)
min_y = min(y for x,y in visited)
max_y = max(y for x,y in visited)

for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
        new_obstacle = {(x,y) : "#"}
        
        current_pos = start_pos
        current_dir = start_dir
        visited = defaultdict(list)
        visited[current_pos].append(current_dir)

        next_pos, next_dir = get_next_move(floorplan | new_obstacle, current_pos, current_dir)
        while True:
            if next_dir in visited[next_pos]:
                print(x,y)
                looped += 1
                break

            elif not is_in_range(floorplan | new_obstacle, current_pos):
                escaped += 1
                break
            
            current_pos, current_dir = next_pos, next_dir
            visited[current_pos].append(current_dir)
            next_pos, next_dir = get_next_move(floorplan | new_obstacle, current_pos, current_dir)

print("Part 2:", looped)
