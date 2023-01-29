import io

test_1 = '...>>>>>...'
test_2 = '''..........
.>v....v..
.......>..
..........'''
test_3 = '''...>...
.......
......>
v.....>
......>
.......
..vvv..'''
test_4 = '''v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>'''

test = test_4

seabed_width = 0
seabed_height = 0
seabed = []


def display_seabed(seabed):
    for row in seabed:
        print(''.join(row))
    print()


def can_move(seabed, herd):
    moving = []

    for y in range(seabed_height):
        for x in range(seabed_width):
            current = seabed[y][x]
            if current == herd:
                if current == 'v':
                    below = (y + 1) % seabed_height
                    if seabed[below][x] == '.':
                        moving += [(y,x)]
                elif current == '>':
                    right = (x + 1) % seabed_width
                    if seabed[y][right] == '.':
                        moving += [(y,x)]

    return moving


def make_move(seabed, moves):
    for move in moves:
        y, x = move
        if seabed[y][x] == 'v':
            below = (y + 1) % seabed_height
            seabed[below][x], seabed[y][x] = 'v', '.' 
        elif seabed[y][x] == '>':
            right = (x + 1) % seabed_width
            seabed[y][right], seabed[y][x] = '>', '.'


def full_step(seabed):
    moved = False
    for herd in ('>', 'v'):
        moving = can_move(seabed, herd)
        make_move(seabed, moving)
        moved = len(moving) > 0

    return moved
    # display_seabed(seabed)

# with io.StringIO(test) as raw:
with open('input25.txt') as raw:
    for line in raw:
        seabed.append(list(line.strip()))
        seabed_height += 1
        seabed_width = max(seabed_width, len(line.strip()))

# print(seabed_width, seabed_height, seabed)
failed_to_move = 1
step = 1
moved = full_step(seabed)
while failed_to_move > 0:
    moved = full_step(seabed)
    if not moved: failed_to_move -= 1
    step += 1

display_seabed(seabed)
print('steps:', step)
