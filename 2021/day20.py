import io

test = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###'''


def find_limits(image):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    for key in image:
        if image[key] == '#':
            min_x = min(min_x, key[0])
            max_x = max(max_x, key[0])
            min_y = min(min_y, key[1])
            max_y = max(max_y, key[1])

    return min_x, min_y, max_x, max_y


def find_neighbours(col, row):
    good_friends = []

    for y in range(row-1, row+2):
        for x in range(col-1, col+2):
            good_friends.append((x, y))

    return good_friends


iea = []
image = {}

# with io.StringIO(test) as inputs:
with open('input20.txt') as inputs:
    iea = list(inputs.readline().strip())
    inputs.readline()

    for y in range(-500, 501):
        for x in range(-500, 501):
            image[(x,y)] = '.'

    row = 0
    for line in inputs:
        for x, ch in enumerate(line.strip()):
            image[(x,row)] = ch
        row += 1

    lx,ly,mx,my = find_limits(image)
    print('original limits:', lx,ly,mx,my)

# print('iea:', iea)
# print('image:', image)

# for y in range(ly-3,my+4):
#     for x in range(lx-3, mx+4):
#         print(image.get((x,y), '#'), end='')
#     print()

##
# due to data, default is '#' on even steps, '.' on even
for steps in range(50):
    new_image = dict(image)
    lx,ly,mx,my = find_limits(image)
    print('new limits:', lx,ly,mx,my)
    for y in range(-200,201):
        for x in range(-200, 201):
            friends = find_neighbours(x, y)
            # print(friends)
            # bits = [image.get(friend, '#' if steps % 2 == 0 else '.') for friend in friends]
            # data = ['1' if image.get(friend, '#' if steps % 2 == 0 else '.') == '#' else '0' for friend in friends]
            bits = [image[friend] for friend in friends]
            data = ['1' if image[friend] == '#' else '0' for friend in friends]
            value = int(''.join(data), 2)
            # print(iea[data])
            new_image[(x,y)] = iea[value]
    image = new_image

final_image = {}
lx,ly,mx,my = find_limits(image)
for y in range(-149,200):
    for x in range(-200, 200):
        final_image[(x,y)] = image.get((x,y),'.')
        print(image.get((x,y),'.'), end='')
    print()

print(len([ch for ch in final_image.values() if ch == '#']))