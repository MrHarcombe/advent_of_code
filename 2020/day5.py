from io import StringIO

test = """FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL"""

# test = "FBFBBFFRLR"

##
# 44, 5  -> 357
# 70, 7  -> 567
# 14, 7  -> 119
# 102, 4 -> 820

def parse_row(row_str):
    lower = (2 ** 0) - 1
    upper = (2 ** 7) - 1

    # print(lower, upper)

    for ch in row_str:
        mid = (upper - lower + 1) // 2
        # print(f"{mid=}")
        if ch == "F":
            upper -= mid
        elif ch == "B":
            lower += mid
            
        # print(ch, "->", lower, upper)
        
    return lower

def parse_seat(seat_str):
    lower = (2 ** 0) - 1
    upper = (2 ** 3) - 1

    # print(lower, upper)

    for ch in seat_str:
        mid = (upper - lower + 1) // 2
        # print(f"{mid=}")
        if ch == "L":
            upper -= mid
        elif ch == "R":
            lower += mid
            
        # print(ch, "->", lower, upper)
        
    return lower


# with StringIO(test) as data:
with open("input5.txt") as data:
    seats = []
    for line in data:
        line = line.strip()
        row = parse_row(line[:7])
        seat = parse_seat(line[7:])

        seats.append(row * 8 + seat)

    print("Part 1:", max(seats))

for seat in sorted(seats):
    if seat+1 not in seats and seat+2 in seats:
        print("Part 2:", seat+1)
