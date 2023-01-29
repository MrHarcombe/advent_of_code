test = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''


def identify_neighbours(map, row, col):
    neighbours = []
    if row > 0:
        neighbours.append((row-1, col))
    if col > 0:
        neighbours.append((row, col-1))
    if col < len(map[0]) - 1:
        neighbours.append((row, col+1))
    if row < len(map) - 1:
        neighbours.append((row+1, col))

    return neighbours

###
# Breadth-first graph traversal
#
#  1  procedure BFS(G, root) is
#  2      let Q be a queue
#  3      label root as explored
#  4      Q.enqueue(root)
#  5      while Q is not empty do
#  6          v := Q.dequeue()
#  7          if v is the goal then
#  8              return v
#  9          for all edges from v to w in G.adjacentEdges(v) do
# 10              if w is not labeled as explored then
# 11                  label w as explored
# 12                  Q.enqueue(w)

# as Python
# visited = [(row,col)]
# queue = []

# queue.append((row,col))

# while len(queue) > 0:
#     row,col = queue.pop()
#     if row == len(map) - 1 and col == len(map[0]) - 1:
#         return visited

#     good_friends = identify_neighbours(map, row, col)
#     for row,col in good_friends:
#         if (row,col) not in visited:
#             visited.append((row,col))
#             queue.append((row,col))


###
# Dijkstra path
#  1  function Dijkstra(Graph, source):
#  2
#  3      create vertex set Q
#  4
#  5      for each vertex v in Graph:            
#  6          dist[v] ← INFINITY                 
#  7          prev[v] ← UNDEFINED                
#  8          add v to Q                     
#  9      dist[source] ← 0                       
# 10     
# 11      while Q is not empty:
# 12          u ← vertex in Q with min dist[u]   
# 13                                             
# 14          remove u from Q
# 15         
# 16          for each neighbor v of u still in Q:
# 17              alt ← dist[u] + length(u, v)
# 18              if alt < dist[v]:              
# 19                  dist[v] ← alt
# 20                  prev[v] ← u
# 21
# 22      return dist[], prev[]


def calculate_paths(map,row,col):
    vertices = {}
    for loop_y in range(len(map)):
        for loop_x in range(len(map[0])):
            #  [0] risk ← INFINITY
            #  [1] prev ← UNDEFINED
            #  [2] visited ← FALSE
            vertices[(loop_y,loop_x)] = [float('inf'), None, False]
    
    # set the risk of origin to 0
    vertices[(row,col)][0] = 0

    while len([cave for cave in vertices if not vertices[cave][2]]) > 0:
        # u ← vertex in Q with min risk[u]
        # print('next ones:', sorted(list(vertices.items()), key=lambda item: item[1][0] if not item[1][2] else (item[1][0] + float('inf'))))
        next_cave = sorted(list(vertices.items()), key=lambda item: item[1][0] if not item[1][2] else (item[1][0] + float('inf')))[0][0]

        # remove u from Q
        vertices[next_cave][2] = True

        if next_cave[0] == len(map) and next_cave[1] == len(map[0]):
            # optimisation to stop when processed the bottom right, regardless (apparently)
            return vertices

        good_friends = identify_neighbours(map, next_cave[0], next_cave[1])
        unvisited_friends = [friend for friend in good_friends if not vertices[friend][2]]
        # for each neighbor v of u still in Q:
        for cave in unvisited_friends:
            # alt ← risk[u] + length(u, v)
            step = vertices[next_cave][0] + map[cave[0]][cave[1]]
            if step < vertices[cave][0]:
                vertices[cave][0] = step
                vertices[cave][1] = next_cave

    return vertices

cave = []
megacave = []

import io
# with io.StringIO(test) as inputs:
with open('input15.txt') as inputs:
    for line in inputs:
        row = [int(n) for n in list(line.strip())]
        cave.append(row)


def new_n(n, x, y):
    new_n = n + x + y
    if new_n <= 9:
        return new_n
    else:
        return new_n - 9


for y in range(5):
    for row in cave:
        megarow = []
        for x in range(5):
            megarow += [new_n(n, x, y) for n in row]
        megacave.append(megarow)

# print(cave)
# print(megacave)

# trace = calculate_paths(cave, 0, 0)
# print(((len(cave)-1),len(cave[0])-1),'->',trace[((len(cave)-1),len(cave[0])-1)])

trace = calculate_paths(megacave, 0, 0)
print(((len(megacave)-1),len(megacave[0])-1),'->',trace[((len(megacave)-1),len(megacave[0])-1)])

# current = trace[((len(cave)-1),len(cave[0])-1)]
# while current[1] != (0,0):
#     print(current[1], '->',trace[current[1]])
#     current = trace[current[1]]
