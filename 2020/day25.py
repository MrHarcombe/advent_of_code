from functools import cache
from io import StringIO

test = """5764801
17807724"""

@cache
def transform(number: int, subject_number: int):
    number = number * subject_number
    number = number % 20201227
    return number

def find_loop_count(number: int):
    cracker = 1
    loop = 0
    while cracker != number:
        cracker = transform(cracker, 7)
        loop += 1
    return loop

# with StringIO(test) as inputs:
with open("input25.txt") as inputs:
    card_public = int(inputs.readline())
    door_public = int(inputs.readline())

card_loops = find_loop_count(card_public)
door_loops = find_loop_count(door_public)

print(f"{card_loops=}, {door_loops=}")

if card_loops < door_loops:
    subject_number = door_public
    loops = card_loops
else:
    subject_number = card_public
    loops = door_loops

encryption_key = 1
for _ in range(loops):
    encryption_key = transform(encryption_key, subject_number)
    # print(encryption_key)

print("Part 1:", encryption_key)
# from reddit, while checking... pow(card_public, door_loops, 20201227)

# too low
# 15992361
# 10441485

# too high
# 20187932