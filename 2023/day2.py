from io import StringIO
from math import prod

test = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

maximums = { "red": 12, "green": 13, "blue": 14 }
p1_total = 0
p2_total = 0

# with StringIO(test) as data:
with open("input2.txt") as data:
    for line in data:
        game, games = line.strip().split(":")
        #print(game, games)
        gid = int(game.split()[1])
        possible = True
        g_max = { "red": 0, "green": 0, "blue": 0 }
        for game in games.split(";"):
            # print("---")
            for cube in game.split(","):
                parts = cube.split()
                count, colour = int(parts[0]), parts[1].strip()
                # print(gid, "->", count, colour)
                if count > maximums[colour]:
                    possible = False
                if count > g_max[colour]:
                    g_max[colour] = count
                        
        if possible:
            p1_total += gid
        p2_total += prod(g_max.values())

print("Part 1:", p1_total)
print("Part 2:", p2_total)
