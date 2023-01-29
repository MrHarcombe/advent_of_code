test = '''2199943210
3987894921
9856789892
8767896789
9899965678'''

seabed = []
low_points = {}

import io
#with io.StringIO(test) as file:
with open('input9.txt') as file:
    for line in file:
        seabed.append([int(n) for n in list(line.strip())])

def locate_neighbours(seabed, row, col):
    neighbours = []
    if row > 0:
        neighbours.append((row-1, col))
    if col > 0:
        neighbours.append((row, col-1))
    if col < len(seabed[0]) - 1:
        neighbours.append((row, col+1))
    if row < len(seabed) - 1:
        neighbours.append((row+1, col))

    return neighbours

'''
Flood-fill (node):
  1. Set Q to the empty queue or stack.
  2. Add node to the end of Q.
  3. While Q is not empty:
  4.   Set n equal to the first element of Q.
  5.   Remove first element from Q.
  6.   If n is Inside:
         Set the n
         Add the node to the west of n to the end of Q.
         Add the node to the east of n to the end of Q.
         Add the node to the north of n to the end of Q.
         Add the node to the south of n to the end of Q.
  7. Continue looping until Q is exhausted.
  8. Return.'''
def flood_fill(seabed, row, col):
    #print('flood_fill:', row, col)
    included = []
    visited = []
    flood_queue = []
    flood_queue.append((row,col))

    while len(flood_queue) != 0:
        row,col = flood_queue.pop()
        visited.append((row,col))
        if seabed[row][col] != 9:
            included.append((row,col))

            if row > 0:
                if (row-1,col) not in visited and (row-1,col) not in flood_queue:
                    flood_queue.append((row-1, col))
            if col > 0:
                if (row,col-1) not in visited and (row,col-1) not in flood_queue:
                    flood_queue.append((row, col-1))
            if col < len(seabed[0]) - 1:
                if (row,col+1) not in visited and (row,col+1) not in flood_queue:
                    flood_queue.append((row, col+1))
            if row < len(seabed) - 1:
                if (row+1,col) not in visited and (row+1,col) not in flood_queue:
                    flood_queue.append((row+1, col))

        #print('included:', len(included), 'flood_queue:', len(flood_queue))

    return included    

for row in range(len(seabed)):
    for col in range(len(seabed[0])):
        lowest = min([seabed[neighbour[0]][neighbour[1]] for neighbour in locate_neighbours(seabed, row, col)])
        if seabed[row][col] < lowest:
            low_points[(row,col)] = seabed[row][col]

#print(seabed)
print('risk:', sum(low_points.values()) + len(low_points.values()))

basins = {}
for row,col in low_points:
    basins[(row,col)] = flood_fill(seabed, row, col)

import math
print('basin area:', math.prod(sorted([len(basin) for basin in basins.values()], reverse=True)[:3]))
