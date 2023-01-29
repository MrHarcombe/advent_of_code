def has_empty_row(grid, tgrid):
    for i in range(5):
        if len(''.join(grid[i])) == 0 or len(''.join(tgrid[i])) == 0:
            return True


def remove_number(number, grid, tgrid):
    for i in range(5):
        if number in grid[i]:
            grid[i][grid[i].index(number)] = ''
        if number in tgrid[i]:
            tgrid[i][tgrid[i].index(number)] = ''


def calculate_sum(grid):
    total = 0
    for i in range(5):
        total += sum([int(n) for n in grid[i] if n])
    return total

with open("input4.txt") as data:
    called = data.readline().strip().split(",")
    print(called)

    grids = []
    while True:
        blank = data.readline()
        if not blank:
            break
        grid = []
        for i in range(5):
            row = data.readline().split()
            grid.append(row)
        grids.append(grid)

    # print(grids, len(grids), len(grids[0]))

# copy and translate horizontal to vertical for all grids
tgrids = []
for grid in grids:
    tgrid = [[] for i in range(5)]
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            tgrid[j].append(value)

    tgrids.append(tgrid)

# print(tgrids)

# now only need to check rows for each grid (length of each row?)
losers = list(range(len(grids)))
print(len(losers),"->",losers)
all_done = False
for call in called:
    if not all_done:
        for i in range(len(grids)):
            remove_number(call, grids[i], tgrids[i])
            if has_empty_row(grids[i], tgrids[i]):
                if len(losers) == 1 and losers[0] == i:
                    print('got last one:', i, call, int(call) * calculate_sum(grids[i]))
                    all_done = True
                    break
                else:
                    print('got one:', i, call, int(call) * calculate_sum(grids[i]))
                    if i in losers:
                        losers.remove(i)
                        print(len(losers),"->",losers)

# print(grids)