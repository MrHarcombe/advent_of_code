large_list = [n for n in range(100)]

#designer = 10
designer = 1358

def is_open(x,y):
    value = x*x + 3*x + 2*x*y + y + y*y
    value += designer
    
    value_binary = f"{value:b}"
    parity = sum([int(ch) for ch in value_binary])
    
    return parity % 2 == 0

def get_neighbours(x,y):
    neighbours = []
    if is_open(x,y):
        if x-1 >= 0:
            if is_open(x-1, y):
                neighbours.append((x-1,y))
        if is_open(x+1,y):
            neighbours.append((x+1,y))
        if y-1 >= 0:
            if is_open(x, y-1):
                neighbours.append((x,y-1))
        if is_open(x,y+1):
            neighbours.append((x,y+1))
    return neighbours        

def breadth_first(start_xy, end_xy):
    discovered = []
    visited = []
    queue = []

    discovered.append(start_xy)
    queue.append([start_xy])
    while len(queue) > 0:
        current_path = queue.pop(0)
        current_node = current_path[-1]

        if current_node == end_xy:
            return current_path

        for neighbour in get_neighbours(current_node[0], current_node[1]):
            if not neighbour in discovered:
                discovered.append(neighbour)
                new_path = list(current_path)
                new_path.append(neighbour)
                queue.append(new_path)

    return large_list

def manhattan_distance(point_a, point_b):
    result = sum([abs(x - y) for x, y in zip(point_a, point_b)])
    return result

# for y in range(7):
#     for x in range(10):
#         print("." if is_open(x,y) else "#", end="")
#     print()
# path = breadth_first((1,1), (7,4))

path = breadth_first((1,1), (31,39))
for y in range(max([y for x,y in path])+1):
    row = []
    for x in range(max([x for x,y in path])+1):
        if is_open(x,y) and (x,y) in path:
            row.append('O')
        elif is_open(x,y):
            row.append('.')
        elif not is_open(x,y):
            row.append('#')
    print(''.join(row))
print(len(path) - 1)

print()
print("---")
print()

destinations = []
for y in range(35):
    row = []
    for x in range(35):
        if is_open(x,y) and len(breadth_first((1,1), (x,y))) <= 51:
            destinations.append((x,y))
            row.append('O')
        elif is_open(x,y):
            row.append('.')
        elif not is_open(x,y):
            row.append('#')
    print(''.join(row))

print(len(destinations))
