from io import StringIO

class Disc:
    def __init__(self, number, positions, initial):
        self.number = number
        self.positions = positions
        self.initial = initial
        
    def get_position(self, time):
        return (self.initial + self.number + time) % self.positions

    def __str__(self):
        return f"#{self.number}, p:{self.positions}, i:{self.initial}"


def parse_disc(line):
    parts = line.split()
    number = int(parts[1][-1])
    positions = int(parts[3])
    initial = int(parts[11][0])
    return Disc(number, positions, initial)


test = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""

discs = []

#with StringIO(test) as f:
with open("input15.txt") as f:
    for line in f:
        discs.append(parse_disc(line))

# part b
discs.append(Disc(7,11,0))

time = 0
total = float("inf")
while total != 0:
    total = sum([disc.get_position(time) for disc in discs])
    time += 1
print(time-1)