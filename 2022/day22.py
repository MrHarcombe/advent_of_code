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

def make_turn(direction, turn):
    if turn == "L":
        return (direction - 1) % 4
    elif turn == "R":
        return (direction + 1) % 4
    else:
        return direction

def get_face(row, column):
    if row <= 49:
        if 50 <= column <= 99:
            return 1, row, column - 50
        elif 100 <= column <= 149:
            return 2, row, column - 100
    elif row <= 99:
        if 50 <= column <= 99:
            return 3, row - 50, column - 50
    elif row <= 149:
        if column <= 49:
            return 4, row - 100, column
        elif 50 <= column <= 99:
            return 5, row - 100, column - 50
    elif row <= 199:
        if column <= 49:
            return 6, row - 150, column
        
    print("uh-oh:", row, column)
    return 99, row, column

def get_neighbour_part2(row, column, direction):
    face, block_row, block_column = get_face(row, column)

    # directions: 0 = R, 1 = D, 2 = L, 3 = U

    # first on current row - next((i for i, ch in enumerate(board[row]) if ch != ' '))
    # last on current row - len(board[row]) - 1
    # first on current column - next((j for j in range(len(board)) if board[j][column] != " "))
    # last on current column - next((j for j in range(len(board)-1,-1,-1) if len(board[j]) > column and board[j][column] != " "))

    if direction == 0: # to the right
        # before end of current row
        if column < len(board[row]) - 1:
            # next on current row
            return row, column + 1, direction

        else:
            if face == 2:
                # warp to right of face 5, turn through 180, current rows down is the new rows up
                direction = 2
                row = next((j for j in range(len(board)-1,-1,-1) if len(board[j]) > (column-50) and board[j][(column-50)] != " ")) - block_row
                column = len(board[row]) - 1
                
            elif face == 3:
                # warp to bottom of face 2, go up, new block column is the current block row
                direction = 3
                column = block_row + 100
                row = next((j for j in range(len(board)-1,-1,-1) if len(board[j]) > column and board[j][column] != " "))
                
            elif face == 5:
                # warp to right of face 2, turn through 180, current rows down is the new rows up
                direction = 2
                row = next((j for j in range(len(board)-1,-1,-1) if len(board[j]) > (column+50) and board[j][(column+50)] != " ")) - block_row
                column = len(board[row]) - 1
                
            elif face == 6:
                # warp to bottom of face 5, go up, new block column is the current block row
                direction = 3
                column = block_row + 50
                row = next((j for j in range(len(board)-1,-1,-1) if len(board[j]) > column and board[j][column] != " "))

            return row, column, direction
                
    elif direction == 2: # to the left
        # after start of current row
        if column > next((i for i, ch in enumerate(board[row]) if ch != ' ')):
            # previous on current row
            return row, column - 1, direction

        else:
            if face == 1:
                # warp to left of face 4, turn 180, current rows down is new rows up
                direction = 0
                row = next((j for j in range(len(board)-1,-1,-1) if len(board[j]) > (column-50) and board[j][(column-50)] != " ")) - 50 - block_row
                column = 0 # next((j for j in range(len(board)) if board[j][column] != " "))

            elif face == 3:
                # warp to top of face 4, go down, new block column is current block row
                direction = 1
                column = block_row
                row = next((j for j in range(len(board)) if board[j][column] != " "))
                
            elif face == 4:
                # warp to left of face 1, turn 180, current rows down is new rows up
                direction = 0
                row = 49 - block_row
                column = next((j for j in range(len(board)) if board[j][column] != " "))

            elif face == 6:
                # warp to top of face 1, turn right, new block column is current block row
                direction = 1
                column = block_row + 50
                row = 0 # next((j for j in range(len(board)) if board[j][column] != " "))

            return row, column, direction

    elif direction == 1: # below
        # not the bottom row with moves in this column
        if row < next((j for j in range(len(board)-1,-1,-1) if len(board[j]) > column and board[j][column] != " ")):
            # move down this column
            return row + 1, column, direction

        else:
            if face == 6:
                # warp to top of face 2, no turn
                row = 0 # next((j for j in range(len(board)) if board[j][column] != " "))
                column = block_column + 100
                
            elif face == 5:
                # warp to right of face 6, go left, new block row is current block column
                direction = 2
                row = block_column + 150
                column = len(board[row]) - 1
                
            elif face == 2:
                # warp to right of face 3, go left, new block row is current block column
                direction = 2
                row = block_column + 50
                column = len(board[row]) - 1

            return row, column, direction
    
    else: # above
        # not the top row with moves in this column
        if row > next((j for j in range(len(board)) if board[j][column] != " ")):
            # move up this column
            return row - 1, column, direction

        else:
            if face == 4:
                # warp to left of face 3, turn left, new block row is current block column
                direction = 0
                row = block_column + 50
                column = next((i for i, ch in enumerate(board[row]) if ch != ' '))

            elif face == 1:
                # warp to left of face 6, turn left, new block row is current block column
                direction = 0
                row = block_column + 150
                column = 0 # next((i for i, ch in enumerate(board[row]) if ch != ' '))

            elif face == 2:
                # warp to bottom of face 6, no turn
                column = block_column
                row = len(board) - 1 # next((j for j in range(len(board)-1,-1,-1) if len(board[j]) > column and board[j][column] != " "))

            return row, column, direction

def get_neighbour(row, column, direction):
    if direction == 0: # to the right
        # at end of current row
        if column == len(board[row]) - 1:
            # return start of current row
            return row, next((i for i, ch in enumerate(board[row]) if ch != ' '))
        else:
            # next on current row
            return row, column + 1
    elif direction == 2: # to the left
        # after start of current row
        if column > next((i for i, ch in enumerate(board[row]) if ch != ' ')):
            # previous on current row
            return row, column - 1
        else:
            # last on current row
            return row, len(board[row]) - 1
    elif direction == 1: # below
        # not the bottom row with moves in this column
        if row < next((j for j in range(len(board)-1,-1,-1) if len(board[j]) > column and board[j][column] != " ")):
            # move down this column
            return row + 1, column
        else:
            # move to the top of the column in this block
            return next((j for j in range(len(board)) if board[j][column] != " ")), column
    else: # above
        # not the top row with moves in this column
        if row > next((j for j in range(len(board)) if board[j][column] != " ")):
            # move up this column
            return row - 1, column
        else:
            # move to the bottom of the column in this block
            return next((j for j in range(len(board)-1,-1,-1) if len(board[j]) > column and board[j][column] != " ")), column

def can_move(row, column):
    # print(row, column)
    return board[row][column] not in ('#', ' ')

def get_direction_character(direction):
    if direction == 0:
        return ">"
    elif direction == 1:
        return "v"
    elif direction == 2:
        return "<"
    else:
        return "^"

board = []
# with StringIO(test) as f:
with open("input22.txt") as f:
    for line in f:
        if line.strip() != "":
            board.append(line.rstrip())
        else:
            break

    instructions = f.readline().strip()

# directions: 0 = R, 1 = D, 2 = L, 3 = U

# find starting position
row = 0
column = next((i for i, ch in enumerate(board[row]) if ch != ' '))
direction = 0

# testing
# row = 0
# column = 100
# direction = 3
# instructions = "5"

# board[row] = board[row][:column] + get_direction_character(direction) + board[row][column+1:]

moves = re.compile(r"(?P<a>[0-9]+)(?P<b>[LR]?)")
for match in moves.finditer(instructions):
    step, turn = match.group(1,2)
    
    print(step, turn)
    for m in range(int(step)):
        print(f"{row:3},{column:3}", board[row][:column].lstrip() + get_direction_character(direction) + board[row][column+1:])
        nr, nc, nd = get_neighbour_part2(row, column, direction)
        # print(row, column, direction, "->", nr, nc, nd)
        if can_move(nr, nc):
            print(f"{row:3},{column:3}", board[nr][:nc].lstrip() + get_direction_character(nd) + board[nr][nc+1:])
            # print("can move")
            row, column, direction = nr, nc, nd
            # board[row] = board[row][:column] + get_direction_character(direction) + board[row][column+1:]
        else:
            print(f"{row:3},{column:3}", board[nr].lstrip())
            # print("can't move")
            break
        # print(row, column, direction)
        input("?")
    direction = make_turn(direction, turn)
    # print(step, turn, "->", row, column, direction)
    # board[row] = board[row][:column] + get_direction_character(direction) + board[row][column+1:]

# print(row, column, direction)
# for display_row in board:
#     print(display_row)

print((row+1) * 1000 + (column+1) * 4 + direction)

# part 1
# 128292 too high
# 11236 too low

# part 2
# 187024 too low
# 95361 too low
# 147121 too low :(
# 43384 still too low :`(
# 135160 again, too low
