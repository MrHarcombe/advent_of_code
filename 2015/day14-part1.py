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

        print(now, distance)

    return distance

race_length = 2503 # 2503 for actual data, 1000 for test data
distances = []

#lines = test_input.split("\n")
with open("day14.txt") as f:
    for line in f:
        if line:
            name, speed, flight_time, rest_time = get_values(line)
            print(name, speed, flight_time, rest_time)
            distance = calculate_distance_travelled(speed, flight_time, rest_time, race_length)
            distances.append(distance)

print("part 1:", max(distances))