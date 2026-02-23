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
    paths = [[origin,origin+(0+1j)]]
    while paths[0][-1].imag <= manifold_height - origin.imag:
        if not len(paths) % 10_000:
            print(f"Up to {len(paths)} paths...")

        path = paths.pop(0)
        tachyon = path[-1]
        if tachyon.imag <= manifold_height - origin.imag:
            if tachyon+(0+1j) in manifold:
                if tachyon.real > 0:
                    new_path = path + [tachyon+(-1+1j)]
                    if new_path not in paths:
                        paths.append(new_path)
                if tachyon.real < manifold_width:
                    new_path = path + [tachyon+(1+1j)]
                    if new_path not in paths:
                        paths.append(new_path)
            else:
                new_path = path + [tachyon+(0+1j)]
                if new_path not in paths:
                    paths.append(new_path)
    
    return len(paths)

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
