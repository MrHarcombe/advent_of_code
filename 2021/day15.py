test = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''

cave = []

import io
# with io.StringIO(test) as inputs:
with open('input15.txt') as inputs:
    for line in inputs:
        row = [int(n) for n in list(line.strip())]
        cave.append(row)

print(cave)


def identify_neighbours(map, row, col):
    neighbours = []
    # if row > 0:
    #     neighbours.append((row-1, col))
    # if col > 0:
    #     neighbours.append((row, col-1))
    if col < len(map[0]) - 1:
        neighbours.append((row, col+1))
    if row < len(map) - 1:
        neighbours.append((row+1, col))

    return neighbours


def calculate_path_risk(map,row,col,typical_risk,risk=0,path=[],queue=[]):
    risk += map[row][col]
    if risk > typical_risk:
        return

    path += [(row,col)]
    if row == len(map)-1 and col == len(map[0])-1:
        # print('yielding path:', risk)
        yield risk, path

    good_friends = identify_neighbours(map, row, col)
    if len(good_friends) == 0:
        return

    # risks = [map[neighbour_row][neighbour_col] for neighbour_row,neighbour_col in good_friends]
    # print('risks:', list(zip(good_friends, risks)))
    # lowest_risk = min(risks)
    # print('min risk:', lowest_risk)
    for neighbour_row, neighbour_col in good_friends:
        # if map[neighbour_row][neighbour_col] == lowest_risk:
        # print('yielding to (', neighbour_row, neighbour_col, ')')
        yield from calculate_path_risk(map, neighbour_row, neighbour_col, typical_risk, risk, path, queue + [(neighbour_row,neighbour_col)])


total_risk = sum([sum([col for col in row]) for row in cave])
average_risk = round((total_risk + 0.5) / (len(cave) * (len(cave[0]) - 1)))
typical_risk = average_risk * (len(cave) + (len(cave[0]) - 1))

# print(identify_neighbours(cave, 0, 0))
# paths = list(calculate_path_risk(cave, 0, 0))
lowest_risk = float('inf')
for path in calculate_path_risk(cave, 0, 0, typical_risk):
    # print('path risk:', path[0])
    if path[0] < lowest_risk:
        lowest_risk = path[0]
    # print('path:', path[1])
    # print('\n\n')
# print('lowest:', min(paths), 'of', len(paths), 'paths')
print('lowest risk:', lowest_risk - cave[0][0])