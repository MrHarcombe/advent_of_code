from io import StringIO
test = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

def find_location(entries):
    for key in almanac:
        lines, all_ranges = almanac[key]

        new_entries = []
        for entry in entries:
            if any([True for s in all_ranges if entry in s]):
                for line in lines:
                    dest, src, rng = line

                    if entry in range(src, src + rng):
                        new_entries.append(dest + (entry - src))
                        # print("Found first match - will there be another?")
                        # break
            else:
                new_entries.append(entry)

            # print("Next seed")

        # print(entries, "->", new_entries)
        entries = new_entries

    return entries

# with StringIO(test) as data:
with open("input5.txt") as data:
    seeds = list(map(int, data.readline().strip().split()[1:]))
    data.readline()

    almanac = {}
    for map_index in range(7):
        # map_name = data.readline().strip()
        data.readline()

        mapping = []
        all_ranges = set()
        line = list(map(int, data.readline().strip().split()))
        while len(line) > 0:
            dest, src, rng = line
            mapping.append([dest, src, rng])
            all_ranges.add(range(src, src + rng))
            line = list(map(int, data.readline().strip().split()))

        almanac[map_index] = (mapping, all_ranges)

# part 1
# locations = find_location(list(seeds))
# print("Part 1:", min(locations), "->", locations)

# part 2
min_location = float("inf")
for i in range(0, len(seeds), 2):
    for seed in range(seeds[i], seeds[i] + seeds[i+1]):
        location = find_location([seed])
        if min(location) < min_location:
            min_location = min(location)
            print("New minimum:", min_location)
print("Part 2:", min_location)
