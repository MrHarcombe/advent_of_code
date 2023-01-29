test = '''.#.#.#
...##.
#....#
..#...
#.#..#
####..'''

board = []

import io
# with io.StringIO(test) as input_board:
with open('input.txt') as input_board:
    for line in input_board:
        row = []
        for i, ch in enumerate(line.strip()):
            row.append(ch)
        board.append(row)

board[0][0] = '#'
board[0][-1] = '#'
board[-1][0] = '#'
board[-1][-1] = '#'
print(board[0], board[-1])

def count_neighbours(board, row, col):
    live_neighbours = 0
    if row > 0:
        live_neighbours += board[row-1][max(col-1,0):col+2].count('#')
        # print(board[row-1][max(col-1,0):col+2].count('#'), 'from row above', end="; ")
    live_neighbours += 1 if col > 0 and board[row][col-1] == '#' else 0
    live_neighbours += 1 if col < len(board[0]) - 1 and board[row][col+1] == '#' else 0
    # print((1 if col > 0 and board[row][col-1] == '#' else 0) + (1 if col < len(board[0]) - 1 and board[row][col+1] == '#' else 0), 'from either side', end='; ')
    if row < len(board) - 1:
        live_neighbours += board[row+1][max(col-1,0):col+2].count('#')
        # print(board[row-1][max(col-1,0):col+2].count('#'), 'from row below', end='; ')

    return live_neighbours

# print(board)

generations = 100   # 4 for test; 100 for live
for step in range(generations):
    new_board = [['.' for col in range(len(board[0]))] for row in range(len(board))]
    for row in range(len(board)):
        for col in range(len(board[row])):
            neighbours = count_neighbours(board, row, col)
            # print(row, col, "->", count_neighbours(board, row, col))
            
            if board[row][col] == '#' and (neighbours < 2 or neighbours > 3):
                new_board[row][col] = '.'
            elif neighbours == 3:
                new_board[row][col] = '#'
            else:
                new_board[row][col] = board[row][col]

            new_board[0][0] = '#'
            new_board[0][-1] = '#'
            new_board[-1][0] = '#'
            new_board[-1][-1] = '#'

    board = new_board
    # print(board)

print(sum([row.count('#') for row in board]))