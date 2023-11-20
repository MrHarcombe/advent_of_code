from io import StringIO
from time import time

test_cavern = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

def get_neighbours(cavern, node):
    for delta in (-1,0), (1,0), (0,-1), (0,1):
        new_neighbour = (node[0]+delta[0], node[1]+delta[1])
        if 0 <= new_neighbour[0] < len(cavern):
            if 0 <= new_neighbour[1] < len(cavern[new_neighbour[0]]):
                yield new_neighbour

### - from wikipedia
#  1  function Dijkstra(Graph, source):

def dijkstra(cavern, start):

#  2      
#  3      for each vertex v in Graph.Vertices:
#  4          dist[v] ← INFINITY
#  5          prev[v] ← UNDEFINED
#  6          add v to Q
#  7      dist[source] ← 0

    distances = {}
    previous = {}
    queue = []
    for row in range(len(cavern)):
        for col in range(len(cavern[0])):
            distances[(row, col)] = float("inf")
            previous[(row, col)] = None
            queue.append((row, col))
            
    distances[(start)] = 0

#  8      
#  9      while Q is not empty:
# 10          u ← vertex in Q with min dist[u]
# 11          remove u from Q
# 12          

    while len(queue) > 0:
        shortest = sorted(distances.items(), key=lambda n:n[1])
        for node, _ in shortest:
            if node in queue:
                queue.remove(node)
                break

# 13          for each neighbor v of u still in Q:
# 14              alt ← dist[u] + Graph.Edges(u, v)
# 15              if alt < dist[v]:
# 16                  dist[v] ← alt
# 17                  prev[v] ← u
# 18

        for neighbour in get_neighbours(cavern, node):
            alt = distances[node] + cavern[neighbour[0]][neighbour[1]]
            if alt < distances[neighbour]:
                distances[neighbour] = alt
                previous[neighbour] = node

# 19      return dist[], prev[]

    return distances, previous
# 

cavern = []

# with StringIO(test_cavern) as data:
with open("input15.txt") as data:
    for line in data:
        cavern.append([int(n) for n in line.strip()])
        
start = (0, 0) # row, column
target = (len(cavern)-1, len(cavern[len(cavern)-1])-1)

begin = time()
distances, previous = dijkstra(cavern, start)
print(distances[target])
print("duration:", time() - begin)