from collections import defaultdict
from io import StringIO

from hexgrid import HexGrid

test = "esew"
test = "nwwswee"
test = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

def tokenise_directions(directions: str):
    direction_list = []
    while len(directions):
        step, directions = directions[0], directions[1:]
        if step in ("e", "w"):
            direction_list.append(step)
        else:
            qualifier, directions = directions[0], directions[1:]
            direction_list.append(step+qualifier)
    return direction_list

floor = HexGrid(False)
origin = floor.get_origin()

# with StringIO(test) as inputs:
with open("input24.txt") as inputs:
    for line in inputs:
        directions = tokenise_directions(line.strip())
        
        tile = origin
        for step in directions:
            tile = floor.get_neighbour(tile, step)
            

        floor[tile] = not floor[tile] if tile in floor else True    

print("Part 1:", sum(floor.values()))

def count_neighbours(floor: HexGrid, tile:tuple):
    black_tiles = 0
    for neighbour in floor.get_neighbours(tile):
        if neighbour in floor and floor[neighbour]:
            black_tiles += 1
    return black_tiles

def process_day(floor: HexGrid):
    to_consider = set()
    black_tiles = [tile for (tile,state) in floor.items() if state]
    for tile in black_tiles:
        to_consider.update(floor.get_neighbours(tile))
    to_consider.update(black_tiles)
    
    to_flip = []
    for tile in to_consider:
        black = count_neighbours(floor, tile)
        if black == 2:
            # flip white tiles to black
            if tile not in floor or not floor[tile]:
                to_flip.append(tile)
                
        elif black == 0 or black > 2:
            # flip black tiles to white
            if tile in floor and floor[tile]:
                to_flip.append(tile)
                
    for tile in to_flip:
        if tile in floor:
            floor[tile] = not floor[tile]
        else:
            floor[tile] = True

for _ in range(100):
    process_day(floor)
    
print("Part 2:", sum(floor.values()))
