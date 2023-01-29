from io import StringIO
import re

test = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

# FACE_SIZE = 4
FACE_SIZE = 50

def roll_on(row, col, direction):
    if direction == 0:
        return row, (col + 1) % FACE_SIZE
    elif direction == 1:
        return (row + 1) % FACE_SIZE, col
    elif direction == 2:
        return row, (col - 1) % FACE_SIZE
    elif direction == 3:
        return (row - 1) % FACE_SIZE, col
    else:
        return row, col

def swap_row(row, col, direction):
    return FACE_SIZE - row - 1, col

def swap_col(row, col, direction):
    return row, FACE_SIZE - col - 1

def row_col_top(row, col, direction):
    return 0, row

def swap_row_col_top(row, col, direction):
    return 0, FACE_SIZE - row - 1

def row_col_end(row, col, direction):
    return FACE_SIZE - 1, row

def swap_row_col_end(row, col, direction):
    return FACE_SIZE - 1, FACE_SIZE - row - 1

def col_row_top(row, col, direction):
    return col, 0

def swap_col_row_top(row, col, direction):
    return FACE_SIZE - col - 1, 0

def col_row_end(row, col, direction):
    return col, FACE_SIZE - 1

def swap_col_row_end(row, col, direction):
    return FACE_SIZE - col - 1, FACE_SIZE - 1

# directions: 0 = R, 1 = D, 2 = L, 3 = U

sample_transitions = {
    (1, 0): (6, 2, swap_row),         (1, 1): (4, 1, roll_on),          (1, 2): (3, 1, row_col_top),      (1, 3): (2, 1, swap_col),
    (2, 0): (3, 0, roll_on),          (2, 1): (5, 3, swap_col),         (2, 2): (6, 3, swap_row_col_end), (2, 3): (1, 1, swap_col),
    (3, 0): (4, 0, roll_on),          (3, 1): (5, 0, swap_col_row_top), (3, 2): (2, 2, roll_on),          (3, 3): (1, 0, col_row_top),
    (4, 0): (6, 1, swap_row_col_top), (4, 1): (5, 1, roll_on),          (4, 2): (3, 2, roll_on),          (4, 3): (1, 3, roll_on),
    (5, 0): (6, 0, roll_on),          (5, 1): (2, 3, swap_col),         (5, 2): (3, 3, swap_row_col_end), (5, 3): (4, 3, roll_on),
    (6, 0): (1, 2, swap_row),         (6, 1): (2, 0, swap_col_row_top), (6, 2): (5, 2, roll_on),          (6, 3): (4, 2, swap_col_row_end)
}

actual_transitions = {
    (1, 0): (2, 0, roll_on),     (1, 1): (3, 1, roll_on),     (1, 2): (4, 0, swap_row),    (1, 3): (6, 0, col_row_top),
    (2, 0): (5, 2, swap_row),    (2, 1): (3, 2, col_row_end), (2, 2): (1,2, roll_on),      (2, 3): (6, 3, roll_on),
    (3, 0): (2, 3, row_col_end), (3, 1): (5, 1, roll_on),     (3, 2): (4, 1, row_col_top), (3, 3): (1, 3, roll_on),
    (4, 0): (5, 0, roll_on),     (4, 1): (6, 1, roll_on),     (4, 2): (1, 0, swap_row),    (4, 3): (3, 0, col_row_top),
    (5, 0): (2, 2, swap_row),    (5, 1): (6, 2, col_row_end), (5, 2): (4, 2, roll_on),     (5, 3): (3, 3, roll_on),
    (6, 0): (5, 3, row_col_end), (6, 1): (2, 1, roll_on),     (6, 2): (1, 1, row_col_top), (6, 3): (4, 3, roll_on)
}

# transitions = sample_transitions
transitions = actual_transitions

def parse_board(board):
    faces = {}
    face_coords = {}
    face = 1
    parse_row = 0
    while face <= 6:
        parse_start = next((i for i, ch in enumerate(board[parse_row]) if ch != ' '))
        while parse_start < len(board[parse_row]):
            grid = [board[row][parse_start:parse_start + FACE_SIZE] for row in range(parse_row, parse_row + FACE_SIZE)]
            faces[face] = grid
            face_coords[face] = (parse_row, parse_start)
            face += 1
            parse_start += FACE_SIZE
        parse_row += FACE_SIZE
    return faces, face_coords

def make_turn(direction, turn):
    if turn == "L":
        return (direction - 1) % 4
    elif turn == "R":
        return (direction + 1) % 4
    else:
        return direction

def get_neighbour(face, row, column, direction):
    if direction == 0 and column != FACE_SIZE - 1:
        # to the right and at end of current row
        # move to next on current row
        return face, row, column + 1, direction

    elif direction == 2 and column != 0:
        # to the left and after start of current row
        # move to previous on current row
        return face, row, column - 1, direction

    elif direction == 1 and row != FACE_SIZE - 1:
        # going down and not on bottom row
        # move down this column
        return face, row + 1, column, direction

    elif direction == 3 and row != 0:
        # going up and not on top row
        # move up this column
        return face, row - 1, column, direction

    # apply face warp transition
    face, direction, op = transitions[(face, direction)]
    tr, tc = op(row, column, direction)
    return face, tr, tc, direction

def can_move(face, row, column):
    # print(row, column)
    return faces[face][row][column] not in ('#', ' ')

board = []
# with StringIO(test) as f:
with open("input22.txt") as f:
    for line in f:
        if line.strip() != "":
            board.append(line.rstrip())
        else:
            break

    instructions = f.readline().strip()

faces, coords = parse_board(board)

# find starting position
face = 1
row = 0
column = 0
direction = 0

# testing
# directions: 0 = R, 1 = D, 2 = L, 3 = U
# face = 2
# row = 0
# column = 0
# direction = 2
# 
# instructions = "1"

moves = re.compile(r"(?P<a>[0-9]+)(?P<b>[LR]?)")
for match in moves.finditer(instructions):
    step, turn = match.group(1,2)

    for m in range(int(step)):
        nf, nr, nc, nd = get_neighbour(face, row, column, direction)
        if can_move(nf, nr, nc):
            face, row, column, direction = nf, nr, nc, nd
        else:
            break

    direction = make_turn(direction, turn)

face_row, face_col = coords[face]
print((face_row+row+1) * 1000 + (face_col+column+1) * 4 + direction)

# part 2
# 187024 too low
# 95361 too low
# 147121 too low :(
# 43384 still too low :`(
# 135160 again, too low
# 128145 - dammit!!
# 189097 !!! Yes !!!
