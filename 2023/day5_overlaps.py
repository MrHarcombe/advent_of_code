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

def find_location2(entry_ranges):
    for key in almanac:
        lines, all_ranges = almanac[key]
        changed_entry_ranges = []

        for line in lines:
            dest, src, rng = line
            unchanged_entry_ranges = []

            for entry_range in entry_ranges:
                if any([True for s in all_ranges if len(range(max(entry_range.start, s.start), min(entry_range.stop, s.stop))) > 0]):
                    # range is all before src
                    if entry_range.stop < src:
                        # continue
                        if entry_range not in unchanged_entry_ranges:
                            unchanged_entry_ranges.append(entry_range)

                    # range starts before src, ends within range
                    elif entry_range.start < src and entry_range.stop > src and entry_range.stop <= src + rng:
                        # split into two
                        if range(entry_range.start, src) not in unchanged_entry_ranges:
                            unchanged_entry_ranges.append(range(entry_range.start, src)) # unchanged before
                        if range(dest, dest + entry_range.stop - src) not in changed_entry_ranges:
                           changed_entry_ranges.append(range(dest, dest + entry_range.stop - src)) # changed within

                    # range starts before src, ends after range
                    elif entry_range.start < src and entry_range.stop > src + rng:
                        # split into three
                        if range(entry_range.start, src) not in unchanged_entry_ranges:
                            unchanged_entry_ranges.append(range(entry_range.start, src)) # unchanged before
                        if range(dest, dest + rng) not in changed_entry_ranges:
                            changed_entry_ranges.append(range(dest, dest + rng)) # changed within
                        if range(src + rng, entry_range.stop) not in unchanged_entry_ranges:
                            unchanged_entry_ranges.append(range(src + rng, entry_range.stop)) # unchanged after

                    # range starts after src, ends within range
                    elif entry_range.start >= src and entry_range.stop <= src + rng:
                        # wholly contained
                        if range(dest + entry_range.start - src, dest + entry_range.start - src + len(entry_range)) not in changed_entry_ranges:
                            changed_entry_ranges.append(range(dest + entry_range.start - src, dest + entry_range.start - src + len(entry_range))) # changed within

                    # range starts after range
                    else:
                        if entry_range not in unchanged_entry_ranges:
                            unchanged_entry_ranges.append(entry_range)
                            # continue

                    # source_range = range(max(entry_range.start, src), min(entry_range.stop, src + rng))
                    # if len(source_range) > 0:
                    #    new_entry_range = range(dest + abs(entry_range.start - src), dest + abs(entry_range.start - src) + len(source_range))
            
                else:
                    if entry_range not in unchanged_entry_ranges:
                        unchanged_entry_ranges.append(entry_range)

            entry_ranges = unchanged_entry_ranges
        entry_ranges = changed_entry_ranges + unchanged_entry_ranges
        
    return [r.start for r in entry_ranges]

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
locations = find_location(list(seeds))
print("Part 1:", min(locations))

# part 2
locations2 = []
for i in range(0, len(seeds), 2):
    locations2 += find_location2([range(seeds[i], seeds[i] + seeds[i+1])])
print("Part 2:", min(locations2))
