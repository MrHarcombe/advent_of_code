from itertools import count
from io import StringIO

test = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

test = """########.
...#.#.##
#..#####.
#..#.....
..##.#...
..##...#.
..##...#.
..##.#...
#.##.....
#..#####.
...#.#.##
########.
##.##.###
....#####
..#.....#
..#.....#
....#####"""

pattern = count(0)
patterns = {}
matches = {}

def transpose_block(block):
    return ["".join([block[y][x] for y in range(len(block))]) for x in range(len(block[0]))]


def find_horizontal(block, ignore=None):
    for flip in range(1, len(block)):
        for p1, p2 in zip(range(flip-1, -1, -1), range(flip, len(block))):
            if block[p1] != block[p2]:
                break
        else:
            if flip != ignore:
                return flip

    return 0

def find_vertical(block, ignore=None):
    return find_horizontal(transpose_block(block), ignore)

# with StringIO(test) as data:
with open("input13.txt") as data:
    block = []
    for line in data:
        if line.strip() == "":
            patterns[next(pattern)] = block
            block = []
        else:
            block.append(line.strip())

    patterns[next(pattern)] = block
    
hor = 0
ver = 0
for pattern in patterns:
    h = v = 0
    h = find_horizontal(patterns[pattern])
    hor += h
    if h == 0:
        v = find_vertical(patterns[pattern])
        ver += v

    matches[pattern] = (h,v)

print("Part 1:", 100 * hor + ver)

def get_possible_smudges(block):
    for row1 in range(len(block)):
        for row2 in range(row1+1, len(block)):
            pos = []
            for i, (ch1,ch2) in enumerate(zip(block[row1], block[row2])):
                if ch1!=ch2:
                    pos.append(i)
            else:
                if len(pos) == 1:
                    yield row1,row2,pos[0]

def toggle(block, line, pos):
    new_block = list(block)
    new_line = list(new_block[line])
    new_line[pos] = "#" if new_block[line][pos] == "." else "."
    new_block[line] = "".join(new_line)
    return new_block

def display_pair(block1, block2):
    for i in range(len(block1)):
        print(block1[i], "\t", block2[i])
    print()

hor = 0
ver = 0
for pattern in patterns:
    block = patterns[pattern]
    for l1, l2, ch in get_possible_smudges(patterns[pattern]):
        block1 = toggle(block, l1, ch)
        # display_pair(block, block1)
        h = v = 0
        h = find_horizontal(block1, matches[pattern][0])
        if h == 0:
            v = find_vertical(block1, matches[pattern][1])
        if (h + v > 0): # and matches[pattern] != (h,v):
            # print(pattern, (h,v))
            break
        
        block2 = toggle(block, l2, ch)
        # display_pair(block, block2)
        h = v = 0
        h = find_horizontal(block2, matches[pattern][0])
        if h == 0:
            v = find_vertical(block2, matches[pattern][1])
        if (h + v > 0):
            # print(pattern, (h,v))
            break
        
    else:
        print("Uh-oh", pattern, [s for s in get_possible_smudges(block)])
        tblock = transpose_block(patterns[pattern])
        for l1, l2, ch in get_possible_smudges(tblock):
            block1 = toggle(tblock, l1, ch)
            # display_pair(block, block1)
            h = v = 0
            h = find_vertical(block1, matches[pattern][0])
            if h == 0:
                v = find_horizontal(block1, matches[pattern][1])
            if (h + v > 0):
                # print(pattern, "transposed", (h,v))
                break
            
            block2 = toggle(tblock, l2, ch)
            # display_pair(block, block2)
            h = v = 0
            h = find_vertical(block2, matches[pattern][0])
            if h == 0:
                v = find_horizontal(block2, matches[pattern][1])
            if (h + v > 0):
                # print(pattern, "transposed", (h,v))
                break
        else:
            print("Uh-oh (transposed)", pattern, [s for s in get_possible_smudges(tblock)])

#         h = v = 0
#         try:
#             h = min([h for h in (h1, h2) if h > 0])
#         except:
#             pass
#         try:
#             v = min([v for v in (v1, v2) if v > 0])
#         except:
#             pass
# 
#         if v > 0:
#             h = 0

    if h + v == 0:
        print("Uh-oh", pattern, [s for s in get_possible_smudges(patterns[pattern])])
    
    # print(h, v)
    hor += h
    ver += v

print("Part 2:", 100 * hor + ver)

# 32455, 36709, 40293, 46708, 48600 too high
# 31969 wrong
# 17523, 19507 too low