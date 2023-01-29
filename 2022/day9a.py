from io import StringIO

test = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

head, tail = (0,0), (0,0)

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

# print(test)
tail_moves = []
# with StringIO(test) as f:
with open("input9.txt") as f:
    for line in f:
        for move in get_moves(head, line):
            if not is_adjacent(move, tail):
                tail = get_tail_move(move, tail)
                tail_moves.append(tail)
        head = move
print(len(set(tail_moves)))

for y in range(max(tail_moves, key=lambda i:i[1])[1]+1):
    for x in range(max(tail_moves, key=lambda i:i[0])[0]+1):
        if (x,y) in tail_moves: print('#', end="")
        else: print(".", end="")
    print()
