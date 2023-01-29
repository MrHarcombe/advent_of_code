import io

map1 = '''..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#'''

input_map = []
right = 1
down = 2
trees = 0

with io.StringIO(map1) as inputs:
    for line in inputs:
        input_map.append(line.strip())

# with open("input3.txt") as inputs:
#     for line in inputs:
#         input_map.append(line.strip())

print(input_map)
pos = (0, 0)
while pos[0] < len(input_map):
    if input_map[pos[0]][pos[1] % len(input_map[0])] == '#':
        trees += 1
        print("ouch")

    pos = (pos[0]+down, pos[1]+right)
    print(pos)

print(trees)