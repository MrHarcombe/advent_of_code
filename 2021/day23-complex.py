from collections import defaultdict
from heapq import heappush, heappop
import io

test = '''#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########'''

def manhattan_distance(pa, pb):
    # distance = sum(abs(p1-p2) for p1, p2 in zip(pa, pb))
    return abs(pa.real - pb.real) + abs(pa.imag - pb.imag)

def build_empty_chamber():
    chamber = {}
    for x in range(1, 12):
        chamber[complex(x, 1)] = '.'
    for x in (3, 5, 7, 9):
        for y in range(2,4):
            chamber[complex(x,y)] = '.'

    return chamber


def parse_initial_places(chamber):
    # with io.StringIO(test) as inputs:
    with open('input23.txt') as inputs:
        for y, line in enumerate(inputs):
            for x, ch in enumerate(line.rstrip()):
                if ch in ('A', 'B', 'C', 'D'):
                    # print(line, x, y, ch)
                    chamber[complex(x, y)] = ch


def display_chamber(chamber):
    for y in range(0, 5):
        for x in range(0,13):
            print(chamber.get(complex(x,y), '#'), end='')
        print()


def all_settled(chamber):
    settled = True

    for i, x in enumerate(['A', 'B', 'C', 'D']):
        if chamber[complex((2*(i+1))+1, 2)] != x or chamber[complex((2*(i+1))+1, 3)] != x:
            settled = False

    return settled


def astar_guess(pos, goal):
    # print(f'guessing from {node} to {goal} as {6 * cityblock(node, goal)}')
    return 1 * manhattan_distance(pos, goal)


def identify_neighbours(chamber, row, col):
    neighbours = []
    if chamber.get(complex(row-1,col), '#') == '.':
        neighbours.append(complex(row-1, col))
    if chamber.get(complex(row, col-1), '#') == '.':
        neighbours.append(complex(row, col-1))
    if chamber.get(complex(row, col+1), '#') == '.':
        neighbours.append(complex(row, col+1))
    if chamber.get(complex(row+1, col), '#') == '.':
        neighbours.append(complex(row+1, col))

    return neighbours


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def calculate_paths(map, start, goal, func):
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

    heappush(open_set, (f_score[start], abs(start), start))

    while len(open_set) > 0:
        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        # current := the node in openSet having the lowest fScore[] value
        current = heappop(open_set)[2]

        # print('considering', current)
        if current == goal:
            # print('at goal')
            return came_from

        for friend in identify_neighbours(map, current.real, current.imag):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_g_score = g_score[current] + 1 # every move only costs 1
            if tentative_g_score < g_score[friend]:
                # This path to neighbor is better than any previous one. Record it!
                came_from[friend] = current
                g_score[friend] = tentative_g_score
                friend_f_score = tentative_g_score + func(friend, goal)
                f_score[friend] = friend_f_score
                if friend not in open_set:
                    heappush(open_set, (friend_f_score, abs(friend), friend))

    # Open set is empty but goal was never reached
    return


def clear_path(chamber, pos, goal):
    return calculate_paths(chamber, pos, goal, astar_guess) != None


def follow_path(chamber, pos, goal):
    result = calculate_paths(chamber, pos, goal, astar_guess)
    if result != None:
        path = reconstruct_path(result, goal)

    # upshot: goal = chamber[pos], pos = '.'
    print(f'moving {chamber[pos]} from {pos} to {goal}')
    print(path)

    chamber[goal], chamber[pos] = chamber[pos], '.'
    return len(path)


def apply_move(chamber, pos, goal):
    result = calculate_paths(chamber, pos, goal, astar_guess)
    if result != None:
        path = reconstruct_path(result, goal)

    # upshot: goal = chamber[pos], pos = '.'
    # print(f'moving {chamber[pos]} from {pos} to {goal}')
    # print(path)

    return len(path) * creature_cost(chamber[pos]), { **chamber, goal : chamber[pos], pos : '.' }


def home_column(creature):
    return (2 * (('A', 'B', 'C', 'D').index(creature) + 1)) + 1


def creature_cost(creature):
    return 10 ** ('A', 'B', 'C', 'D').index(creature)

def move_home(chamber, fella_pos):
    home_col = home_column(chamber[fella_pos])
    fella_cost = creature_cost(chamber[fella_pos])

    # either there's a clear path to the bottom of the home column,
    # or the creature already at the bottom of the home column is the
    # same as you and there's a clear path to the top of the home
    # column
    if clear_path(chamber, fella_pos, complex(home_col, 3)):
        return True, follow_path(chamber, fella_pos, complex(home_col, 3)) * fella_cost
        # return [(fella_pos, (home_col, 3))]

    elif ((chamber[fella_pos]) == chamber[complex(home_col, 3)]) and clear_path(chamber, fella_pos, complex(home_col, 2)):
        return True, follow_path(chamber, fella_pos, complex(home_col, 2)) * fella_cost
        # return [(fella_pos, (home_col, 2))]

    return False, 0


def moves_into_corridor(chamber, fella_pos):
    moves = []

    for i in range(1, 12):
        if i not in (3, 5, 7, 9):
            if clear_path(chamber, fella_pos, complex(i, 1)):
                moves.append((fella_pos, complex(i, 1)))

    if len(moves) > 0:
        return moves

def move_into_corridor(chamber, fella_pos):
    # ideally move to left of own home
    # - if on top of own friend AND if home column currently has another incorrect creature at the bottom
    #   move back another column (or -1 if already at left-most)
    # - if way left is blocked, move to right instead
    # - if moving to right, and on top of another, move across an extra column (or +1 if at right-most)
    home_col = home_column(chamber[fella_pos])
    fella_cost = creature_cost(chamber[fella_pos])

    if home_col != 9:
        ideal_destination = [home_col - 1, 1]

        if chamber[complex(home_col, 2)] != chamber[fella_pos]:
            ideal_destination[0] -= 2

        if chamber[complex(home_col, 3)] != chamber[fella_pos]:
            if ideal_destination[0] > 2:
                ideal_destination[0] -= 2
            else:
                ideal_destination[0] -= 1

        while not clear_path(chamber, fella_pos, complex(*ideal_destination)) and ideal_destination[0] <= 10:
            if ideal_destination[0] < 2:
                ideal_destination[0] += 1
            elif ideal_destination[0] < 10:
                ideal_destination[0] += 2
            else:
                ideal_destination[0] += 1

        if clear_path(chamber, fella_pos, complex(*ideal_destination)):
            cost = follow_path(chamber, fella_pos, complex(*ideal_destination)) * fella_cost
            return True, cost

        else:
            print(f"Not moving {chamber[fella_pos]} from {fella_pos}")

    else:
        ideal_destination = [home_col + 1, 1]

        if chamber[complex(home_col, 2)] != chamber[fella_pos]:
            ideal_destination.real += 2

        if chamber[complex(home_col, 3)] != chamber[fella_pos]:
            if ideal_destination[0] > 8:
                ideal_destination[0] += 2
            else:
                ideal_destination[0] += 1

        while not clear_path(chamber, fella_pos, complex(*ideal_destination)) and ideal_destination[0] >= 2:
            if ideal_destination[0] > 10:
                ideal_destination[0] -= 1
            elif ideal_destination[0] > 2:
                ideal_destination[0] -= 2
            else:
                ideal_destination[0] -= 1

        if clear_path(chamber, fella_pos, complex(*ideal_destination)):
            cost = follow_path(chamber, fella_pos, complex(*ideal_destination)) * fella_cost
            return True, cost

        else:
            print(f"Not moving {chamber[fella_pos]} from {fella_pos}")

    return False, 0


def can_move(chamber, fella_pos):
    home_col = home_column(chamber[fella_pos])

    # in bottom row, with someone on top
    if fella_pos.imag == 3 and chamber[complex(fella_pos.real, 2)] != '.':
        return False

    # already home on bottom
    elif fella_pos == complex(home_col, 3):
        return False

    # already home with friend underneath
    elif fella_pos == complex(home_col, 2) and (chamber[fella_pos] == chamber[complex(home_col, 3)]):
        return False

    # someone else in a home column
    elif fella_pos.imag == 1 and (chamber[complex(home_col, 2)] not in (chamber[fella_pos], '.') or chamber[complex(home_col, 3)] not in (chamber[fella_pos], '.')):
        return False

    # in corrdor and no clear path to home
    elif fella_pos.imag == 1 and not (clear_path(chamber, fella_pos, complex(home_col, 2))):
        return False

    return True
    

def find_moves(chamber):
    for fella in ('A', 'B', 'C', 'D'):
        for pos in range(37):
            x = (pos % 12) + 1
            y = (pos // 12) + 1
            # print(f'{pos}, {x}, {y}')

            if chamber[complex(x,y)] == fella:
                # print(f'found {chamber[(x,y)]} at {x,y}')
                if can_move(chamber, complex(x,y)):
                    moved, move_cost = move_home(chamber, complex(x,y))
                    if moved: return move_cost
                    moved, move_cost = move_into_corridor(chamber, complex(x,y))
                    if moved: return move_cost


def make_move(chamber):
    for fella in ('A', 'B', 'C', 'D'):
        for pos in range(37):
            x = (pos % 12) + 1
            y = (pos // 12) + 1
            # print(f'{pos}, {x}, {y}')

            if chamber.get(complex(x,y), '#') == fella:
                # print(f'found {chamber[(x,y)]} at {x,y}')
                if can_move(chamber, complex(x,y)):
                    moved, move_cost = move_home(chamber, complex(x,y))
                    if moved: return move_cost
                    moved, move_cost = move_into_corridor(chamber, complex(x,y))
                    if moved: return move_cost


chamber = build_empty_chamber()
parse_initial_places(chamber)
display_chamber(chamber)

total_cost = 0
while not all_settled(chamber):
    total_cost += make_move(chamber)
    display_chamber(chamber)
    input()
print('total cost:', total_cost)
