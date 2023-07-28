from io import StringIO

test = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
"""

def find_turn(maze, pos, direction):
    if direction[0] != 0:
        above = (pos[0],pos[1]-1)
        below = (pos[0],pos[1]+1)
        if above in maze and (maze[above].isalpha() or maze[above] == "|"):
            return (0,-1)
        elif below in maze and (maze[below].isalpha() or maze[below] == "|"):
            return (0,1)
        else:
            print("Huh?")
    else:
        left = (pos[0]-1,pos[1])
        right = (pos[0]+1,pos[1])
        if left in maze and (maze[left].isalpha() or maze[left] == "-"):
            return (-1,0)
        elif right in maze and (maze[right].isalpha() or maze[right] == "-"):
            return (1,0)
        else:
            print("Huh?")

maze = {}
start = None

# with StringIO(test) as data:
with open("input19.txt") as data:
    row = 0
    for line in data:
        for col, pipe in enumerate(line.rstrip()):
            if pipe != " ":
                maze[(col, row)] = pipe
                if row == 0:
                    start = (col, row)
        row += 1

direction = (0,1)
pos = start
letters = []
steps = 0
while pos in maze:
    if maze[pos] == "+":
        direction = find_turn(maze, pos, direction)
    elif maze[pos].isalpha():
        letters.append(maze[pos])
    
    pos = (pos[0] + direction[0], pos[1] + direction[1])
    steps += 1
    
print("Part 1:", "".join(letters))
print("Part 2:", steps)