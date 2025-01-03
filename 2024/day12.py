from collections import defaultdict
from io import StringIO

directions = {
    0: (0, -1),
    1: (1, -1),
    2: (1, 0),
    3: (1, 1),
    4: (0, 1),
    5: (-1, 1),
    6: (-1, 0),
    7: (-1, -1),
}


def get_neighbours(point):
    x, y = point
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        yield x + dx, y + dy


# def find_matching_neighbours(plot, crop, point):
#     """Finds all matching neighbours, indexed from 0 (top), 1 (top-right), 2 (right), etc. Similarly returns all
#        non-matching neighbours.

#     Args:
#         plot (set): collection of crops to check
#         crop (str): type of crop to match
#         point (tuple(int,int)): coordinate of crop to find for

#     Yields:
#         set: collection of indexes indicating which neighbours are of the same type
#         set: collection of indexes indicating which neighbours are of another type
#     """
#     same_crop = set()
#     other_crop = set()
#     x, y = point

#     # look at the diagonals
#     for direction in (1,3,5,7):
#     for ix, dx, dy in enumerate((0, -1), (1, 0), (0, 1), (-1, 0)):
#         neighbour = plot[(x + dx, y + dy)]
#         if neighbour == crop:
#             same_crop.add(ix)
#         elif neighbour != ".":
#             other_crop.add(ix)

#     return same_crop, other_crop


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


def count_corners(subplot):
    total_corners = 0
    for point in subplot:
        corners = 0
        for diagonal in (1, 3, 5, 7):
            x, y = point
            dix, diy = directions[diagonal]
            adjacent = tuple(
                (x + directions[d][0], y + directions[d][1])
                for d in ((diagonal - 1) % 8, (diagonal + 1) % 8)
            )
            all_in = [a in subplot for a in adjacent]
            all_not_in = [a not in subplot for a in adjacent]
            if (x + dix, y + diy) not in subplot and (all(all_in) or all(all_not_in)):
                corners += 1
            elif (x + dix, y + diy) in subplot and all(all_not_in):
                corners += 1

        # This is the case of an internal square currounded by 4 convex corners
        # if corners == 4 and len(subplot) != 1:
        #     print("4 corners on", point, "in subplot of size", len(subplot))

        total_corners += corners

    return total_corners


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

test = """AAAAAGGRRAA
AAAAAGGGRRR
AAAAAGGARAA
AAAAAGGAAAA
AAAGGGAAAAA
GAAGGGGAAAA
GGGGGGGGAAA
GGGGGGGGGAA
GGGGGGGGAAA
GGGGGGGGGGG"""

test = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

test = """IINNNNIIIIIIIII
INNNNNIIIEIIIII
IIIIEEEEEEIIIII
IIIIIEEEEEIIIII
IIIIEEEEEEEEEII
IIEEEEEEEEEEEII
IIENEEEEEEEEEII
IEEEEEEEEEEEEEM
IIELEEEEEEEEEEM
UEEEEEEEEEEEEEM
UUEEEEEEEELELLM
UUUUEEEEEELLLLM
UZEEEEEEEELLLLL
UEEEEEEEEELLLLL
JEEEEEEEELLLLLL
ICCELEEEELLLLLL
ICCCEEEEELLLLLL
IIIEEEEELLLLLLL
IIEEEEEEEELVLLL
IIBEEEDDKELVVDL
IIIDREDVDEVVVDL
IIIDDDDDDDVVDDD"""


plot = defaultdict(list)

# with StringIO(test) as input_data:
with open("input12.txt") as input_data:
    for y, row in enumerate(input_data):
        for x, ch in enumerate(row.strip()):
            plot[ch].append((x, y))

cost1 = 0
cost2 = 0

total_area = 0

for ch in plot:
    visited = set()
    for point in plot[ch]:
        if point not in visited:
            subplot = find_subplot(plot, ch, point)
            assert len(visited & subplot) == 0
            visited |= subplot
            area = len(subplot)
            total_area += area
            perimeter = find_perimeter(plot, ch, subplot)
            cost1 += area * perimeter
            corners = count_corners(subplot)
            cost2 += area * corners
            print(ch, area, perimeter, corners)

print("Part 1:", cost1)
print("Part 2:", cost2)
print("Total area:", total_area)

# 845490 too low
