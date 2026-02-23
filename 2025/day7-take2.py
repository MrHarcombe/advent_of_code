from collections import defaultdict
from io import StringIO

test = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

def part1(manifold, manifold_width, manifold_height, origin):
    split_count = 0
    tachyons = [origin+(0+1j)]
    tachyon_queue = [origin+(0+1j)]
    while len(tachyon_queue):
        tachyon = tachyon_queue.pop(0)
        if tachyon.imag < manifold_height:
            if tachyon+(0+1j) in manifold:
                split_count += 1
                if tachyon.real > 0 and tachyon+(-1+1j) not in tachyons:
                    tachyons.append(tachyon+(-1+1j))
                    tachyon_queue.append(tachyon+(-1+1j))
                if tachyon.real < manifold_width and tachyon+(1+1j) not in tachyons:
                    tachyons.append(tachyon+(1+1j))
                    tachyon_queue.append(tachyon+(1+1j))
            elif tachyon+(0+1j) not in tachyons:
                tachyons.append(tachyon+(0+1j))
                tachyon_queue.append(tachyon+(0+1j))
    
    return split_count

def part2(manifold, manifold_width, manifold_height, origin):
    tachyon_queue = [origin+(0+1j)]
    tachyons = defaultdict(int)
    tachyons[origin+(0+1j)] = 1

    while len(tachyon_queue):
        tachyon = tachyon_queue.pop(0)
        if tachyon.imag < manifold_height:
            if tachyon+(0+1j) in manifold:
                if tachyon.real > 0:
                    tachyons[tachyon+(-1+1j)] += tachyons[tachyon]
                    if tachyon+(-1+1j) not in tachyon_queue:
                        tachyon_queue.append(tachyon+(-1+1j))
                if tachyon.real < manifold_width:
                    tachyons[tachyon+(1+1j)] += tachyons[tachyon]
                    if tachyon+(1+1j) not in tachyon_queue:
                        tachyon_queue.append(tachyon+(1+1j))
            else:
                tachyons[tachyon+(0+1j)] += tachyons[tachyon]
                if tachyon+(0+1j) not in tachyon_queue:
                    tachyon_queue.append(tachyon+(0+1j))

            # if tachyon in tachyons:
            #     del tachyons[tachyon]
    
    return sum(v for k,v in tachyons.items() if k.imag == manifold_height)

manifold = defaultdict(lambda: ".")
origin = None

# with StringIO(test) as file:
with open("input7.txt") as file:
    for y, line in enumerate(file):
        for x, ch in enumerate(line.strip()):
            if ch == "S":
                origin = complex(x,y)
                manifold[complex(x,y)] = "S"
            elif ch == "^":
                manifold[complex(x,y)] = "^"

manifold_height = y
manifold_width = x

print("Part 1:", part1(manifold, manifold_width, manifold_height, origin))
print("Part 2:", part2(manifold, manifold_width, manifold_height, origin))
