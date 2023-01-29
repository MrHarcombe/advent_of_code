from io import StringIO

test = """30373
25512
65332
33549
35390"""

grid = []

# with StringIO(test) as f:
with open("input8.txt") as f:
    for line in f:
        grid.append([int(n) for n in list(line.strip())])

#print(grid)
visible = 0
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if y == 0 or y == len(grid) - 1 or x == 0 or x == len(grid[y]) - 1:
            visible += 1
            continue

        #print(x,y,"->",grid[y][x])
        #before = visible
        if max(grid[y][:x]) < grid[y][x]:
            visible += 1
        elif max(grid[y][x+1:]) < grid[y][x]:
            visible += 1
        elif max([grid[n][x] for n in range(len(grid)) if n < y]) < grid[y][x]:
            visible += 1
        elif max([grid[n][x] for n in range(len(grid)) if n > y]) < grid[y][x]:
            visible += 1
        #if before != visible:
            #print("it was visible")

print(visible)