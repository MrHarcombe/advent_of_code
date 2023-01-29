import io

MAX_Y = 6
MAX_X = 50

def display_grid(grid):
    for y in range(MAX_Y):
        for x in range(MAX_X):
            print(grid[y][x], end="")
        print()
    print("---")

def set_rectangle(grid, x, y):
    for ry in range(y):
        for rx in range(x):
            grid[ry][rx] = '#'

def rotate_row(grid, row, offset):
    grid[row] = grid[row][-offset:] + grid[row][:-offset]

def rotate_column(grid, column, offset):
    new_col = [grid[row][column] for row in range(MAX_Y)]
    new_col = new_col[-offset:] + new_col[:-offset]
    
    for row in range(MAX_Y):
        grid[row][column] = new_col[row]

# run on a 7 by 3 screen
test = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""

# with io.StringIO(test) as f:
with open("input8.txt") as f:
    grid = [['.' for x in range(MAX_X)] for y in range(MAX_Y)]
    
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            set_rectangle(grid, *[int(n) for n in parts[1].split('x')])
        
        elif parts[1] == "column":
            rotate_column(grid, int(parts[2].split('=')[1]), int(parts[4]))
        
        elif parts[1] == "row":
            rotate_row(grid, int(parts[2].split('=')[1]), int(parts[4]))
        
        else:
            print("uh-oh")

count = 0
for y in range(MAX_Y):
    for x in range(MAX_X):
        if grid[y][x] == '#':
            count += 1
print(count)
display_grid(grid)
