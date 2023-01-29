from io import StringIO

test = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

blocks = [["0011110"],["0001000","0011100","0001000"],["0011100","0000100","0000100"],["0010000","0010000","0010000","0010000"],["0011000","0011000"]]
tower = []
block_cycle = 0
wind_cycle = 0

def display_tower():
    for row in tower[::-1]:
        print(row.replace("0",".").replace("2","#"))
    print("\n")

def can_move_right(bottom_row):
    can_move = True
    for row in tower[bottom_row:]:
        if "1" in row and (row.rindex("1") == len(row)-1 or row[row.rindex("1")+1] == "2"):
            can_move = False

    return can_move

def move_right(bottom_row):
    for row in range(bottom_row, len(tower)):
        row_list = list(tower[row])
        for i in range(5, -1, -1):
            if row_list[i] == "1" and row_list[i+1] == "0":
                row_list[i], row_list[i+1] = row_list[i+1], row_list[i]
        tower[row] = "".join(row_list)

def can_move_left(bottom_row):
    can_move = True
    for row in tower[bottom_row:]:
        if "1" in row and (row.index("1") == 0 or row[row.index("1") - 1] == "2"):
            can_move = False

    return can_move

def move_left(bottom_row):
    for row in range(bottom_row, len(tower)):
        row_list = list(tower[row])
        for i in range(1, 7):
            if row_list[i] == "1" and row_list[i-1] == "0":
                row_list[i], row_list[i-1] = row_list[i-1], row_list[i]
        tower[row] = "".join(row_list)

def check_collision(bottom_row):
    for row in range(bottom_row, len(tower)):
        for i in (n for n, ch in enumerate(tower[row]) if ch == "1"):
            if tower[row-1][i] == "2":
                return True
    return False

def drop_down(bottom_row):
    for row in range(bottom_row, len(tower)):
        upper_list = list(tower[row])
        lower_list = list(tower[row-1])
        for i in (n for n, ch in enumerate(upper_list) if ch == "1"):
            if lower_list[i] != "0":
                print(f"!!! emergency {block_cycle, row} !!!")
            upper_list[i], lower_list[i] = lower_list[i], upper_list[i]
        tower[row] = "".join(upper_list)
        tower[row-1] = "".join(lower_list)

    while sum([int(ch) for ch in tower[-1]]) == 0:
        del tower[-1]

# with StringIO(test) as f:
with open("input17.txt") as f:
    currents = f.readline().strip()

# for i in range(2022):
for i in range(10000):
    next_block = blocks[block_cycle % len(blocks)]
    next_block_base = len(tower)
    tower += next_block

    for i in range(3):
        next_current = currents[wind_cycle % len(currents)]
        wind_cycle += 1

        # print(tower[next_block_base:], "->", end=" ")
        
        if next_current == ">" and can_move_right(next_block_base):
            move_right(next_block_base)

        elif next_current == "<" and can_move_left(next_block_base):
            move_left(next_block_base)

        # print(tower[next_block_base:])

    hit = False
    while not hit:
        next_current = currents[wind_cycle % len(currents)]
        wind_cycle += 1

        # print(tower[next_block_base:], "->", end=" ")

        if next_current == ">" and can_move_right(next_block_base):
            move_right(next_block_base)

        elif next_current == "<" and can_move_left(next_block_base):
            move_left(next_block_base)

        # print(tower[next_block_base:])
        
        if next_block_base == 0:
            hit = True
            for row in range(next_block_base, len(tower)):
                tower[row] = "".join(["0" if n == "0" else "2" for n in tower[row]])

        else:
            hit = check_collision(next_block_base)
            if hit:
                for row in range(next_block_base-1, len(tower)):
                    tower[row] = "".join(["0" if ch == "0" else "2" for ch in tower[row]])

            else:
                drop_down(next_block_base)
                next_block_base -= 1

    with open("heights.csv", "a") as csv:
        print(block_cycle, block_cycle % len(blocks), wind_cycle % len(currents), len(tower), sep=",", file=csv)
    block_cycle += 1

print(len(currents), len(tower))

# print(height + len(tower), (height + len(tower)) * 1000000000000 // len(test) * len(blocks))
