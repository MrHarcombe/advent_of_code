from io import StringIO

test = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""

def rotate(pattern):
    if len(pattern) == 2:
        return [pattern[1][0]+pattern[0][0],pattern[1][1]+pattern[0][1]]
    else:
        return [pattern[2][0]+pattern[1][0]+pattern[0][0],pattern[2][1]+pattern[1][1]+pattern[0][1],pattern[2][2]+pattern[1][2]+pattern[0][2]]

def flip(pattern):
    return [line[::-1] for line in pattern]

def flatten_and_match(pattern):
    size = len(pattern)
    patterns = two_patterns if size == 2 else three_patterns

    flat = "/".join(pattern)
    # print(flat)
    for _ in range(3):
        if flat in patterns:
            return patterns[flat]
        pattern = rotate(pattern)
        flat = "/".join(pattern)
        # print(flat)

    if flat in patterns:
        return patterns[flat]
    else:
        pattern = flip(pattern)
        flat = "/".join(pattern)
        # print(flat)
        for _ in range(3):
            if flat in patterns:
                return patterns[flat]
            pattern = rotate(pattern)
            flat = "/".join(pattern)
            # print(flat)

        if flat in patterns:
            return patterns[flat]

def unflatten(pattern):
    return pattern.split("/")

# def chunk_pattern(pattern):
#     if len(pattern) % 2 == 0:
#         size = len(pattern) // 2
#         chunks = []
#         for rows in range(0, len(pattern), 2):
#             for cols in range(0, len(pattern), 2):
#                 chunks.append([pattern[rows][cols:cols+2],pattern[rows+1][cols:cols+2]])

#     else:
#         assert(len(pattern) % 3 == 0)
#         size = len(pattern) // 3
#         chunks = []
#         for rows in range(0, len(pattern), 3):
#             for cols in range(0, len(pattern), 3):
#                 chunks.append([pattern[rows][cols:cols+3],pattern[rows+1][cols:cols+3],pattern[rows+2][cols:cols+3]])

def get_chunk(pattern, size, chunk_row, chunk_col):
    if size == 2:
        return [
                pattern[chunk_row][chunk_col:chunk_col+2],
                pattern[chunk_row+1][chunk_col:chunk_col+2]
               ]

    else:
        return [
                pattern[chunk_row][chunk_col:chunk_col+3],
                pattern[chunk_row+1][chunk_col:chunk_col+3],
                pattern[chunk_row+2][chunk_col:chunk_col+3]
               ]

def expand_chunks(flat_chunks, pattern):
    size = len(unflatten(flat_chunks[0]))
    for row in range(size):
        new_row = []
        for chunk in flat_chunks:
            new_row.append(unflatten(chunk)[row])

        pattern.append("".join(new_row))        

two_patterns = {}
three_patterns = {}

# with StringIO(test) as data:
with open("2017/input21.txt") as data:
    for line in data:
        match, to = line.split(" => ")
        if match.index("/") == 2:
            two_patterns[match] = to.strip()
        else:
            three_patterns[match] = to.strip()

# print(two_patterns, three_patterns)

start = [".#.","..#","###"]

def expand_pattern(pattern, iterations):
    current = list(pattern)
    for i in range(iterations):
        size = 2 if len(current) % 2 == 0 else 3
        new_pattern = []
        for rows in range(0, len(current), size):
            new_chunks = []
            for cols in range(0, len(current), size):
                chunk = get_chunk(current, size, rows, cols)
                new_chunks.append(flatten_and_match(chunk))

            expand_chunks(new_chunks, new_pattern)

        current = new_pattern

    return current

print("Part 1:", "".join(expand_pattern(start, 5)).count("#"))
print("Part 2:", "".join(expand_pattern(start, 18)).count("#"))

# print(current)
# count = 0
# for line in current:
#     count += line.count("#")
# print("Part 1:", count)
