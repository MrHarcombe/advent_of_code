test = "flqrgnkx"
actual = "vbqugkhl"

def knot_hash(kh_input):
    lengths = [ord(n) for n in kh_input] + [17, 31, 73, 47, 23]
    loop = [n for n in range(256)]

    skip = 0
    position = 0

    for rnd in range(64):
        for step in lengths:
            sub = []
            for n in range(step):
                sub.append(loop[(position + n) % len(loop)])
            for n in range(step):
                loop[(position + n) % len(loop)] = sub.pop()
            
            position = (position + step + skip) % len(loop)
            skip += 1

    dense = []
    for i in range(0, len(loop), 16):
        value = loop[i]
        for j in range(i+1, i+16):
            value ^= loop[j]
        dense.append(f"{value:02x}")

    return "".join(dense)

def get_neighbours(cell, hash_grid):
    neighbours = []
    for dx,dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        x = cell[0] + dx
        y = cell[1] + dy
        if (x,y) in hash_grid:
            neighbours.append((x,y))
            
    return neighbours

hash_grid = {}
prefix = actual
for row in range(128):
    hash_row = knot_hash(f"{prefix}-{row}")
    value = f"{int(hash_row, 16):0128b}"
    for col in range(128):
        if value[col] == "1":
            hash_grid[(col,row)] = "#"

# print(hash_grid)
# for y in range(8):
#     for x in range(8):
#         print(hash_grid.get((x,y), "."), end="")
#     print()

regions = 0
while len(hash_grid) > 0:
    region = set()
    first = next(iter(hash_grid.keys()))
    regions += 1
    
    queue = [first]
    while len(queue) > 0:
        current = queue.pop(0)
        region.add(current)
        neighbours = get_neighbours(current, hash_grid)
        for neighbour in neighbours:
            if neighbour not in region:
                queue.append(neighbour)

    for cell in region:
        del hash_grid[cell]

print(regions)