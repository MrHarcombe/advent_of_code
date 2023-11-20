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

def dijkstra(cavern, start):
    queue = { (row,col) : [float("inf"), None, False] for col in range(len(cavern[0])) for row in range(len(cavern)) }
    queue[start][0] = 0

    while len([n for n in queue if not queue[n][2]]) > 0:
        node = sorted(queue.items(), key=lambda n:(n[1][2],n[1][0]))[0][0]
        queue[node][2] = True

        for neighbour in get_neighbours(cavern, node):
            alt = queue[node][0] + cavern[neighbour[0]][neighbour[1]]
            if alt < queue[neighbour][0]:
                queue[neighbour][0] = alt
                queue[neighbour][1] = node

    return queue

cavern = []

# with StringIO(test_cavern) as data:
with open("input15.txt") as data:
    for line in data:
        cavern.append([int(n) for n in line.strip()])
        
start = (0, 0) # row, column
target = (len(cavern)-1, len(cavern[len(cavern)-1])-1)

begin = time()
results = dijkstra(cavern, start)
print(results[target][0])
print("duration:", time() - begin)