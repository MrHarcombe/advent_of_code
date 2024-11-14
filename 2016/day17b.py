from hashlib import md5
from time import time

large_list = [n for n in range(100)]

OPEN = "bcdef"

def get_neighbours(x, y, hashkey):
    neighbours = []

    hash_neighbours = md5(hashkey.encode()).hexdigest()[:4]

    if y-1 > -1 and hash_neighbours[0] in OPEN:
        neighbours.append(((x,y-1), "U"))
    if y+1 < 4 and hash_neighbours[1] in OPEN:
        neighbours.append(((x,y+1), "D"))
    if x-1 > -1 and hash_neighbours[2] in OPEN:
        neighbours.append(((x-1,y), "L"))
    if x+1 < 4 and hash_neighbours[3] in OPEN :
        neighbours.append(((x+1,y), "R"))
    
    return neighbours        

def shortest_breadth_first(start_xy, end_xy, hashprefix):
    discovered = []
    queue = []

    discovered.append((start_xy, hashprefix))
    queue.append([(start_xy, hashprefix)])
    while len(queue) > 0:
        current_path = queue.pop(0)
        current_node, hashkey = current_path[-1]

        # print("processing", current_node, hashkey)

        if current_node == end_xy:
            return current_path

        neighbours = get_neighbours(current_node[0], current_node[1], hashkey)
        # print("neighbours:", neighbours)

        for neighbour, direction in neighbours:
            if not (neighbour, hashkey + direction) in discovered:
                discovered.append((neighbour, hashkey + direction))
                new_path = list(current_path)
                new_path.append((neighbour, hashkey + direction))
                queue.append(new_path)

def depth_first(start_xy, end_xy, hashprefix):
    visited = []
    stack = []

    stack.append((start_xy, hashprefix))
    while len(stack) > 0:
        current_node, hashkey = stack.pop()
        visited.append((current_node, hashkey))

        if current_node == end_xy:
            yield visited

        else:
            neighbours = get_neighbours(current_node[0], current_node[1], hashkey)
            # print("neighbours:", neighbours)

            for neighbour, direction in neighbours:
                next_neighbour = (neighbour, hashkey + direction)
                if not next_neighbour in visited:
                    stack.append(next_neighbour)

    yield visited


start = time()
# prefix = "ihgpwlah"
# prefix = "kglvqrro"
# prefix = "ulqzkmiv"
prefix = "pslxynzg"
max_length = 0
paths = depth_first((0,0), (3,3), prefix)
for path in paths:
    # print("path:", path[-1][1][len(prefix):])
    # print("length:", len(path[-1][1]) - len(prefix))
    max_length = max(max_length, len(path[-1][1]) - len(prefix))
print(max_length)
print("Time:", time() - start)
