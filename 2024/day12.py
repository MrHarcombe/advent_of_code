from collections import defaultdict
from io import StringIO


def get_neighbours(point):
    x, y = point
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        yield x + dx, y + dy


def find_matching_neighbours(plot, crop, point):
    """Finds all matching neighbours, indexed from 0 (top), 1 (top-right), 2 (right), etc. Similarly returns all non-matching neighbours.

    Args:
        plot (set): collection of crops to check
        crop (str): type of crop to match
        point (tuple(int,int)): coordinate of crop to find for

    Yields:
        set: collection of indexes indicating which neighbours are of the same type
        set: collection of indexes indicating which neighbours are of another type
    """
    same_crop = set()
    other_crop = set()
    x, y = point
    for ix, dx, dy in enumerate((0, -1), (1, 0), (0, 1), (-1, 0)):
        neighbour = plot[(x + dx, y + dy)]
        if neighbour == crop:
            same_crop.add(ix)
        elif neighbour != ".":
            other_crop.add(ix)

    return same_crop, other_crop


def find_subplot(plot, crop, point):
    subplot = set()
    queue = [point]
    while len(queue) > 0:
        current = queue.pop(0)
        subplot.add(current)
        for neighbour in get_neighbours(current):
            if (
                neighbour in plot[crop]
                and neighbour not in queue
                and neighbour not in subplot
            ):
                queue.append(neighbour)
    return subplot


def find_perimeter(plot, crop, subplot):
    perimeter = 0
    for point in subplot:
        point_perimeter = 4
        for neighbour in get_neighbours(point):
            if neighbour in plot[crop]:
                point_perimeter -= 1
        perimeter += point_perimeter
    return perimeter


def count_corners(plot, subplot, crop, point):
    corners = 0
    for point in subplot:
        neighbours = find_matching_neighbours(plot, crop, point)
        if len(neighbours) == 0:
            corners = 4
        elif len(neighbours) == 1:
            assert neighbours[0] % 2 == 0
            corners = 2
        elif len(neighbours) == 2:
            # adjacent or parallel?
            pass
        else:
            # 3 or 4 matching neighbours is a surrounded crop, so no corners
            pass
    return corners


test = """AAAA
BBCD
BBCC
EEEC"""

test = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

test = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

plot = defaultdict(list)

with StringIO(test) as input_data:
    # with open("input12.txt") as input_data:
    for y, row in enumerate(input_data):
        for x, ch in enumerate(row.strip()):
            plot[ch].append((x, y))

cost1 = 0
cost2 = 0

for ch in plot:
    visited = set()
    for point in plot[ch]:
        if point not in visited:
            subplot = find_subplot(plot, ch, point)
            assert len(visited & subplot) == 0
            visited |= subplot
            area = len(subplot)
            perimeter = find_perimeter(plot, ch, subplot)
            cost1 += area * perimeter
            corners = count_corners(plot, ch, subplot)
            cost2 += area * corners
            print(ch, area, perimeter, corners)

print("Part 1:", cost1)
print("Part 2:", cost2)
