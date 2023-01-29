from collections import defaultdict
from io import StringIO

test = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

test = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

knots = {}
for k in range(10):
    knots[k] = (0,0)

directions = { "U" : (0,1), "D" : (0,-1), "L" : (-1,0), "R" : (1,0) }

def get_moves(position, command):
    # print(position, command)
    direction, amount = command.split()
    dx,dy = directions[direction]
    x,y = position
    for times in range(int(amount)):
        x += dx
        y += dy
        yield (x,y)
        
def is_adjacent(head, tail):
    x1,y1 = head
    x2,y2 = tail
    
    return x2-1 <= x1 <= x2+1 and y2-1 <= y1 <= y2+1

def get_tail_move(head, tail):
    hx, hy = head
    tx, ty = tail
    
    if hx == tx:
        ty += 1 if hy > ty else -1
        return (tx, ty)
    elif hy == ty:
        tx += 1 if hx > tx else -1
        return (tx, ty)
    else:
        tx += 1 if hx > tx else -1
        ty += 1 if hy > ty else -1
        return (tx, ty)

knot_moves = defaultdict(list)
for k in range(10):
    knot_moves[k].append((0,0))

# with StringIO(test) as f:
with open("input9.txt") as f:
    for line in f:
        for move in get_moves(knots[0], line):
            previous = move
            # print(previous)
            for knot in range(1,10):
                if not is_adjacent(previous, knots[knot]):
                    previous = get_tail_move(previous, knots[knot])
                    # print("not adjacent, previous:", previous)
                    knots[knot] = previous
                    knot_moves[knot].append(previous)
                else:
                    previous = knots[knot]
        knots[0] = move

print(len(set(knot_moves[9])))

# for y in range(max(knot_moves[9], key=lambda i:i[1])[1]+1):
#     for x in range(max(knot_moves[9], key=lambda i:i[0])[0]+1):
#         if (x,y) in knot_moves[9]: print('#', end="")
#         else: print(".", end="")
#     print()
