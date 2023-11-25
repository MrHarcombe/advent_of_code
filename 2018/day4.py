from collections import Counter
from io import StringIO

class timestamp:

    def __init__(self, value):
        hours, minutes = value.split(":")
        self.hours = int(hours)
        self.minutes = int(minutes)

    def inc(self):
        self.minutes += 1
        if self.minutes == 60:
            self.minutes = 0
            self.hours += 1

    def __eq__(self, other):
        return self.minutes == other.minutes and self.hours == other.hours

    def __str__(self):
        return f"{self.hours:02}:{self.minutes:02}"


test = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""

guard_log = []

# with StringIO(test) as data:
with open("input4.txt") as data:
    for line in data:
        guard_log.append(line.strip())

guard = None
asleep = None
rota = {}
for entry in sorted(guard_log):
    parts = entry.split()

    if parts[2] == "Guard":
        guard = parts[3]
    
    elif parts[2] == "falls":
        asleep = timestamp(parts[1][:-1])
    
    elif parts[2] == "wakes":
        log_date = parts[0][1:]
        awake = timestamp(parts[1][:-1])

        if guard not in rota:
            rota[guard] = {}
        
        if log_date not in rota[guard]:
            rota[guard][log_date] = []

        while asleep != awake:
            rota[guard][log_date].append(asleep.minutes)
            asleep.inc()

part1_counts = []
part2_counts = []
for guard in rota:
    counter = Counter()
    for date in rota[guard]:
        counter.update(rota[guard][date])
    part1_counts.append((counter.total(), int(guard[1:]), counter))
    part2_counts.append((counter.most_common(1)[0][1], int(guard[1:]), counter))

part1 = sorted(part1_counts)[-1]
print("Part 1:", part1[1]*part1[2].most_common(1)[0][0])

part2 = sorted(part2_counts)[-1]
print("Part 2:", part2[1]*part2[2].most_common(1)[0][0])
