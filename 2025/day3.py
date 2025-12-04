from io import StringIO
from time import time

test = """987654321111111
811111111111119
234234234234278
818181911112111"""

def part1(batteries):
    joltage = 0
    
    for battery in batteries:
        upper = max(battery[:-1])
        lower = max(battery[battery.index(upper)+1:])
    
        joltage += upper * 10 + lower
        
    return joltage

def part2(batteries, size=12):
    joltage = 0
    
    for battery in batteries:
        new_joltage = 0
        previous = -1
        for cell in range(size):
            window = len(battery) - size - (previous - cell)
            value = max(battery[previous+1:previous+1+window])
            previous = battery.index(value, previous+1)
            new_joltage = new_joltage * 10 + value

        # print(new_joltage)
        joltage += new_joltage
        
    return joltage

batteries = []

# with StringIO(test) as file:
with open("input3.txt") as file:
    for battery in file:
        batteries.append(list(map(int, list(battery.strip()))))

begin = time()
print("Part 1:", part2(batteries))
print("Elapsed:", time() - begin)
begin = time()
print("Part 2:", part2(batteries))
print("Elapsed:", time() - begin)
