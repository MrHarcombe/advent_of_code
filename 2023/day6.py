from io import StringIO

test = """Time:      7  15   30
Distance:  9  40  200"""

# with StringIO(test) as data:
with open("input6.txt") as data:
    line = data.readline().strip()
    times = map(int, line[line.index(":")+1:].split())
    p2_time = int("".join(line[line.index(":")+1:].split()))
    line = data.readline().strip()
    distances = map(int, line[line.index(":")+1:].split())
    p2_distance = int("".join(line[line.index(":")+1:].split()))

    races = zip(times, distances)
    total_wins = 1
    for race in races:
        time, record = race
        push = 1
        total_wins *= sum([1 for push in range(time) if push * (time - push) > record])
        
print("Part 1:", total_wins)
print("Part 2:", sum([1 for push in range(p2_time) if push * (p2_time - push) > p2_distance]))
