from io import StringIO

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

# with StringIO(test) as data:
with open("input3.txt") as data:
    y = 0
    for line in data:
        for x, ch in enumerate(line.strip()):
            if ch != ".":
                schematic[(y,x)] = ch
        y += 1

def part1():
    symbols = [p for p in schematic.items() if not p[1].isdigit()]
    total = 0
    counted_pos = set()
    for pos, _ in symbols:
        py, px = pos
        for dy,dx in (-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1):
            new_pos = (py+dy, px+dx)
            if new_pos not in counted_pos and schematic.get(new_pos, ".").isdigit():
                # print(new_pos)
                left = 1
                while schematic.get((py+dy, px+dx-left), ".").isdigit():
                    left += 1
                right = 1
                while schematic.get((py+dy, px+dx+right), ".").isdigit():
                    right += 1
                svalue = ""
                for span in range(px+dx-left+1,px+dx+right):
                    counted_pos.add((py+dy,span))
                    svalue += schematic[(py+dy,span)]
                # print(svalue)
                total += int(svalue)
            
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
            if new_pos not in counted_pos and schematic.get(new_pos, ".").isdigit():
                # print(new_pos)
                left = 1
                while schematic.get((py+dy, px+dx-left), ".").isdigit():
                    left += 1
                right = 1
                while schematic.get((py+dy, px+dx+right), ".").isdigit():
                    right += 1
                svalue = ""
                for span in range(px+dx-left+1,px+dx+right):
                    counted_pos.add((py+dy,span))
                    svalue += schematic[(py+dy,span)]
                # print(svalue)
                gear_values.append(int(svalue))
        
        if len(gear_values) == 2:
            g1, g2 = gear_values
            total += g1*g2
    
    print("Part 2:", total)

# part1()
part2()