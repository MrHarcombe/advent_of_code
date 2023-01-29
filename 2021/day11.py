from functools import reduce

small_test = '''11111
19991
19191
19991
11111'''

larger_test = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''

cavern = []

import io
# with io.StringIO(larger_test) as inputs:
with open('input11.txt') as inputs:
    for row in inputs:
        cavern.append([int(n) for n in row.strip()])

def identify_neighbours(cavern,row,col):
    good_friends = []

    # max(..., 0) -> don't go off the top of the grid
    # min(..., len(cavern)) don't go off the bottom of the grid
    for y in range(max(row-1, 0), min(row+2, len(cavern))):
        # similarly don't go off the left or right of the grid
        for x in range(max(col-1, 0), min(col+2, len(cavern[0]))):
            good_friends.append((y, x))

    return good_friends

def step(cavern):
    # part one, increment all enrgy levels
    new_cavern = [[col+1 for col in row] for row in cavern]
    # print(new_cavern)

    max_flashes = len(cavern) * len(cavern[0])

    # part two, while there are octopii > 9, keep flashing
    flashes = 0
    while max([max(row) for row in new_cavern]) > 9:
        affected_neighbours = []
        for row in range(len(new_cavern)):
            for col in range(len(new_cavern[0])):
                if new_cavern[row][col] > 9:
                    flashes += 1
                    new_cavern[row][col] = 0
                    affected_neighbours += identify_neighbours(new_cavern, row, col)

        # print(new_cavern, affected_neighbours)

        for row,col in affected_neighbours:
            # print(row,col, len(new_cavern), len(new_cavern[0]))
            if new_cavern[row][col] != 0:
                new_cavern[row][col] += 1

        # print(display_cavern(new_cavern))
    return new_cavern, flashes, flashes == max_flashes

def display_cavern(cavern):
    out = '\n'
    for row in cavern:
        out += ' '.join([str(n) for n in row])
        out += '\n'
    return out

generations = 500
total_flashes = 0

print('in:', display_cavern(cavern))
for i in range(generations):
    cavern, flashes, in_sync = step(cavern)
    total_flashes += flashes
    if in_sync:
        print(f"*** Synchronised at {i+1} ***")
print('out:', display_cavern(cavern))
print('flashes:', total_flashes)
