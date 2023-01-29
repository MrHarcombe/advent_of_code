import io, operator

test_input = """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

def get_values(line):
    words = line.split()
    name = words[0]
    speed = int(words[3])
    flight_time = int(words[6])
    rest_time = int(words[-2])

    return name, speed, flight_time, rest_time

def calculate_distance_travelled(speed, flight_time, rest_time, time):
    now = 0
    distance = 0
    while now < time:
        if now + flight_time <= time:
            distance += speed * flight_time
            now += flight_time
        else:
            distance += speed * (time - now)
            now = time

        if now + rest_time <= time:
            now += rest_time
        else:
            now = time

        # print(now, distance)

    return distance

race_length = 10 # 2503 for actual data, 1000 for test data
competitors = {}
distances = {}
scores = {}

#lines = test_input.split("\n")
with io.StringIO(test_input) as f:
#with open("input.txt") as f:
    for line in f:
        name, speed, flight_time, rest_time = get_values(line)
        # print(name, speed, flight_time, rest_time)
        competitors[name] = [speed, flight_time, rest_time]
        distances[name] = 0
        scores[name] = 0

for i in range(race_length):
    for name in competitors:
        values = competitors[name]
        distances[name] = calculate_distance_travelled(values[0], values[1], values[2], i+1)
    
        heats = sorted(list(distances.items()), key=operator.itemgetter(1))
    print(heats)
