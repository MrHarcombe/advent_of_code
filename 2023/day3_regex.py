from io import StringIO
import re

test = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

schematic = {}
pattern = re.compile(r'([0-9]+)|([^\.])')

# with StringIO(test) as data:
with open("input3.txt") as data:
    for y, line in enumerate(data):
        for match in pattern.finditer(line.strip()):
            if match.group(0).isdigit():
                hits = (int(match.group(0)), set())
                for sx in range(match.start(), match.end()):
                    hits[1].add((y,sx))
                    schematic[(y,sx)] = hits
            else:
                schematic[(y,match.start())] = match.group(0)

def part1():
    symbols = [p for p in schematic.items() if type(p[1]) is str]
    total = 0
    counted_pos = set()
    for pos, _ in symbols:
        py, px = pos
        for dy,dx in (-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1):
            new_pos = (py+dy, px+dx)
            if new_pos not in counted_pos and type(schematic.get(new_pos, ".")) is tuple:
                value, value_pos = schematic[new_pos]
                # print(pos, value, value_pos)
                total += value
                counted_pos |= value_pos
            
    print("Part 1:", total)

def part2():
    symbols = [p for p in schematic.items() if not p[0] == "*"]
    total = 0
    for pos, _ in symbols:
        counted_pos = set()
        gear_values = []
        py, px = pos
        
        for dy,dx in (-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1):
            new_pos = (py+dy, px+dx)
            if new_pos not in counted_pos and type(schematic.get(new_pos, ".")) is tuple:
                value, value_pos = schematic[new_pos]
                # print(pos, value, value_pos)
                gear_values.append(value)
                counted_pos |= value_pos

        if len(gear_values) == 2:
            g1, g2 = gear_values
            total += g1*g2
    
    print("Part 2:", total)

part1()
part2()