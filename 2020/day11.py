from io import StringIO

test = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

occupancy_test = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""

occupancy_test = """.............
.L.L.#.#.#.#.
............."""

occupancy_test = """.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##."""


initial_seats = {}

# with StringIO(test) as data:
with open("input11.txt") as data:
    for row, line in enumerate(data):
        for col, place in enumerate(line.strip()):
            if place != ".":
                initial_seats[(row,col)] = place

initial_seats["MAX_ROW"] = row
initial_seats["MAX_COL"] = col

def p1_adjacent_occupied_count(seats, row, col):
    return len([seat for dr, dc in ((-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)) if (seat := seats.get((row+dr,col+dc), ".")) == "#"])

def p2_adjacent_occupied_count(seats, start_row, start_col):
    adjacent = []
    for dr, dc in ((-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)):
        next_in_direction = "."
        row = start_row
        col = start_col
        while next_in_direction == ".":
            row += dr
            col += dc
            if 0 <= row <= seats["MAX_ROW"] and 0 <= col <= seats["MAX_COL"]:
                next_in_direction = seats.get((row,col), ".")
                if next_in_direction != ".":
                    adjacent.append(next_in_direction)
            else:
                break

    return adjacent.count("#")

def cycle(seats, f_adjacent, unset_count):
    new_seats = {"MAX_ROW":seats["MAX_ROW"], "MAX_COL": seats["MAX_COL"]}
    for row in range(seats["MAX_ROW"]+1):
        for col in range(seats["MAX_COL"]+1):
            current = seats.get((row,col), ".")
            current_neighbours = f_adjacent(seats, row, col)
            if current == "L":
                if current_neighbours == 0:
                    new_seats[(row,col)] = "#"
                else:
                    new_seats[(row,col)] = "L"
            elif current == "#":
                if current_neighbours >= unset_count:
                    new_seats[(row,col)] = "L"
                else:
                    new_seats[(row,col)] = "#"
    return new_seats

def display_seats(seats):
    for row in range(seats["MAX_ROW"]+1):
        display = []
        for col in range(seats["MAX_COL"]+1):
            current = seats.get((row,col), ".")
            display += current
        print("".join(display))
    print()
    print()

seats = dict(initial_seats)
previous_pattern = ""
seat_pattern = str(sorted(((k,v)) for k,v in seats.items() if isinstance(k, tuple)))

while previous_pattern != seat_pattern:
    # display_seats(seats)
    previous_pattern = seat_pattern
    seats = cycle(seats, p1_adjacent_occupied_count, 4)
    seat_pattern = str(sorted(((k,v)) for k,v in seats.items() if isinstance(k, tuple)))

display_seats(seats)
print("Part 1:", sum(s == "#" for s in seats.values()))

seats = dict(initial_seats)
previous_pattern = ""
seat_pattern = str(sorted(((k,v)) for k,v in seats.items() if isinstance(k, tuple)))

while previous_pattern != seat_pattern:
    # display_seats(seats)
    previous_pattern = seat_pattern
    seats = cycle(seats, p2_adjacent_occupied_count, 5)
    seat_pattern = str(sorted(((k,v)) for k,v in seats.items() if isinstance(k, tuple)))

display_seats(seats)
print("Part 2:", sum(s == "#" for s in seats.values()))
