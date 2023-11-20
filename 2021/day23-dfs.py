from collections import defaultdict
from heapq import heappush, heappop
from io import StringIO
from sys import stdout
from time import time

test = '''#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########'''

partial = """#############
#.D.D...B...#
###.#.#C#.###
###A#B#C#A###
#############"""

go_home = '''#############
#B..........#
###.#.#.#.###
  #.#B#.#.#
  #########'''

open_corridor = '''#############
#...........#
###.#.#.#.###
  #C#.#.#.#
  #########'''

blocked_corridor = '''#############
#.......D...#
###.#.#.#.###
  #C#.#.#.#
  #########'''

nearly = '''#############
#A..C.D...B.#
###.#.#.#.###
  #A#B#C#D#
  #########'''


finished = '''#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########'''

actual = '''#############
#...........#
###C#A#D#D###
  #B#A#B#C#
  #########'''

extra = '''#############
#...........#
###C#A#D#D###
  #D#C#B#A#
  #D#B#A#C#
  #B#A#B#C#
  #########'''


def parse_chamber(data):
    chamber = {}
    row = 0
    for line in data:
        for col, ch in enumerate(line.rstrip()):
            if ch not in (" ", "#"):
                chamber[(row, col)] = ch
        row += 1
        
    return chamber

def display_chamber(chamber, trace=stdout):
    for y in range(0, max_rows+2):
        for x in range(0, max_cols+2):
            print(chamber.get((y, x), '#'), end='', file=trace)
        print(file=trace)


def is_settled(chamber, amphi_pos):
    amphi_col = home_column(chamber.get(amphi_pos))
    if amphi_col != amphi_pos[1]: return False

    settled = True
    in_place = {chamber.get((row, amphi_col), '#') for row in range(amphi_pos[0], bottom_home+1)}
    if len(in_place - {chamber.get(amphi_pos), '#'}) != 0:
        settled = False

    return settled


def all_settled(chamber):
    settled = True

    for i, amphi in enumerate(['A', 'B', 'C', 'D']):
        in_place = {chamber.get((row, 2 * (i + 1) + 1), '#') for row in (2,3,4,5)}
        if len(in_place - {amphi, '#'}) != 0:
            settled = False

    return settled


def astar_guess(pos, goal):
  # print(f'guessing from {node} to {goal} as {6 * cityblock(node, goal)}')
  # return 1 * cityblock(pos, goal)
  return sum([abs(p1 - p2) for p1, p2 in zip(pos, goal)])


def identify_neighbours(chamber, row, col):
    for dy, dx in (-1, 0), (0, -1), (0, 1), (1, 0):
        new_pos = (row+dy, col+dx)
        if chamber.get(new_pos, "#") == ".":
            yield new_pos


def reconstruct_path(came_from, current):
  total_path = [current]
  while current in came_from:
    current = came_from[current]
    total_path.insert(0, current)
  return total_path


def a_star(map, start, goal, func):
  # print(start, goal)

  # The set of discovered nodes that may need to be (re-)expanded.
  # Initially, only the start node is known.
  # This is usually implemented as a min-heap or priority queue rather than a hash-set.
  # openSet = {start}
  open_set = []

  # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
  # to n currently known.
  came_from = {}

  # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
  g_score = defaultdict(lambda: float('inf'))
  g_score[start] = 0

  # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
  # how short a path from start to finish can be if it goes through n.
  f_score = defaultdict(lambda: float('inf'))
  f_score[start] = func(start, goal)

  heappush(open_set, (f_score[start], start))

  while len(open_set) > 0:
    # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
    # current := the node in openSet having the lowest fScore[] value
    current = heappop(open_set)[1]

    # print('considering', current)
    if current == goal:
      # print('at goal')
      return came_from

    for friend in identify_neighbours(map, current[0], current[1]):
      # d(current,neighbor) is the weight of the edge from current to neighbor
      # tentative_gScore is the distance from start to the neighbor through current
      tentative_g_score = g_score[current] + 1  # every move only costs 1
      if tentative_g_score < g_score[friend]:
        # This path to neighbor is better than any previous one. Record it!
        came_from[friend] = current
        g_score[friend] = tentative_g_score
        friend_f_score = tentative_g_score + func(friend, goal)
        f_score[friend] = friend_f_score
        if friend not in open_set:
          heappush(open_set, (friend_f_score, friend))

  # Open set is empty but goal was never reached
  return


def check_path(chamber, pos, goal):
    result = a_star(chamber, pos, goal, astar_guess)
    if result != None:
        return reconstruct_path(result, goal)


def apply_move(chamber, pos, goal):
    return {
        **chamber,
        goal: chamber[pos],
        pos: "."
    }


def home_column(creature):
  return (2 * (('A', 'B', 'C', 'D').index(creature) + 1)) + 1


def creature_cost(creature):
  return 10**('A', 'B', 'C', 'D').index(creature)


def find_valid_corridor_moves(chamber, amphi_pos):
    if amphi_pos[0] > 1:
        move_cost = creature_cost(chamber[amphi_pos])
        
        for i in range(1, 12):
            if i not in (3, 5, 7, 9):
                path = check_path(chamber, amphi_pos, (1, i))
                if path != None:
                    yield (amphi_pos, (1, i), (len(path)-1) * move_cost)


def find_valid_home_moves(chamber, amphi_pos):
    home_col = home_column(chamber[amphi_pos])

    # either there's a clear path to the bottom of the home column,
    # or the creature(s) already at the bottom of the home column
    # is/are the same as you and there's a clear path to the top of
    # the home column
    target_row = bottom_home
    while chamber.get((target_row, home_col), ".") == chamber[amphi_pos]:
        target_row -= 1

    if target_row > corridor and amphi_pos[1] != home_col:
        if chamber.get((target_row, home_col), ".") == ".":
            move_cost = creature_cost(chamber[amphi_pos])
            path = check_path(chamber, amphi_pos, (target_row, home_col))
            if path != None:
                yield (amphi_pos, (target_row, home_col), (len(path)-1) * move_cost)


def find_valid_moves(chamber):
    for row in range(max_rows+1):
        for col in range(max_cols+1):
            if chamber.get((row, col), '#') in ["A", "B", "C", "D"]:
                if not is_settled(chamber, (row, col)):
                    # print(f'found {chamber[(row,col)]} at {row,col}')
                    yield from find_valid_home_moves(chamber, (row, col))
                    yield from find_valid_corridor_moves(chamber, (row, col))


start = time()
with StringIO(extra) as data:
    chamber = parse_chamber(data)

max_rows = max((k[0] for k in chamber))
max_cols = max((k[1] for k in chamber))

corridor = 1
top_home = 2
bottom_home = max_rows

# trace = open("amphipods.txt", "w")
# display_chamber(chamber, trace)
# trace = stdout
best_cost = float("inf")
best_moves = None
discovered = defaultdict(lambda:list())
discovered[f"{sorted(chamber.items())}"].append(0)
queue = [(move, chamber, 0, [move]) for move in find_valid_moves(chamber)]
while len(queue) > 0:
    move, chamber, current_cost, moves = queue.pop(0)
    src, dest, move_cost = move
    current_cost += move_cost
    next_chamber = apply_move(chamber, src, dest)

    # print(src, dest, current_cost, file=trace)
    # display_chamber(next_chamber, trace)
    # input()
    
    if all_settled(next_chamber):
        # print("Found a solution:", current_cost, file=trace)
        if current_cost < best_cost:
            best_cost = current_cost
            best_moves = moves

    else:
        if f"{sorted(next_chamber.items())}" in discovered:
            if min(discovered[f"{sorted(next_chamber.items())}"]) <= current_cost:
                # print("Skipping as already seen cheaper", f"{sorted(next_chamber.items())}", file=trace)
                continue

        if current_cost < best_cost:
            discovered[f"{sorted(next_chamber.items())}"].append(current_cost)
            for next_move in find_valid_moves(next_chamber):
                queue.append((next_move, next_chamber, current_cost, moves + [next_move]))

# trace.close()
print(best_cost, best_moves)
print("Elapsed:", time() - start)

#     for possible in find_valid_home_moves(chamber, (1,1)):
#         if possible != None:
#             dest, cost = possible
#             print("dest:", dest, "cost:", cost)

#     for possible in find_valid_corridor_moves(chamber, (3,3)):
#         if possible != None:
#             dest, cost = possible
#             print("dest:", dest, "cost:", cost)
