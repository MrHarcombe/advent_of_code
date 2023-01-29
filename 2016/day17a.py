from hashlib import md5

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
            yield current_path

        neighbours = get_neighbours(current_node[0], current_node[1], hashkey)
        # print("neighbours:", neighbours)

        for neighbour, direction in neighbours:
            if not (neighbour, hashkey + direction) in discovered:
                discovered.append((neighbour, hashkey + direction))
                new_path = list(current_path)
                new_path.append((neighbour, hashkey + direction))
                queue.append(new_path)

    return large_list

def breadth_first(start_xy, end_xy, hashprefix):
    discovered = []
    visited = []
    queue = []

    discovered.append((start_xy, hashprefix))
    queue.append((start_xy, hashprefix))
    while len(queue) > 0:
        current_node, hashkey = queue.pop(0)
        visited.append((current_node, hashkey))
        # print("processing", current_node, hashkey)

        if current_node == end_xy:
            yield visited

        neighbours = get_neighbours(current_node[0], current_node[1], hashkey)
        # print("neighbours:", neighbours)

        for neighbour, direction in neighbours:
            next_neighbour = (neighbour, hashkey + direction)
            if not next_neighbour in discovered:
                discovered.append(next_neighbour)
                queue.append(next_neighbour)

    return visited

def depth_first(start_xy, end_xy, hashprefix):
    discovered = []
    visited = []
    stack = []

    discovered.append((start_xy, hashprefix))
    stack.append((start_xy, hashprefix))
    while len(stack) > 0:
        current_node, hashkey = stack.pop()
        visited.append((current_node, hashkey))

        if current_node == end_xy:
            yield visited

        neighbours = get_neighbours(current_node[0], current_node[1], hashkey)
        # print("neighbours:", neighbours)

        for neighbour, direction in neighbours:
            next_neighbour = (neighbour, hashkey + direction)
            if not next_neighbour in discovered:
                discovered.append(next_neighbour)
                stack.append(next_neighbour)
    
    return visited


if __name__ == "__main__":
    prefix = "ihgpwlah"
    #prefix = "pslxynzg"
    first = False
    paths = []
    for path in shortest_breadth_first((0,0), (3,3), prefix):
        if not first:
            print(path)
            first = True
        print(len(path[-1][1]) - len(prefix), end=" ")
        paths.append(path)
    print()
    
    print("shortest:", min(paths, key=lambda p: len(p[-1][1])) - len(prefix))
    print("longest:", max(paths,  key=lambda p: len(p[-1][1])) - len(prefix))
