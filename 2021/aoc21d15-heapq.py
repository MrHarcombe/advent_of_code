from io import StringIO
from heapq import heappush, heappop, heapify
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
    cavern_height = len(cavern)
    cavern_width = len(cavern[0])
    
    for dx, dy in (-1,0), (1,0), (0,-1), (0,1):
        new_neighbour = (node[0]+dx, node[1]+dy)
        if 0 <= new_neighbour[0] < cavern_height:
            if 0 <= new_neighbour[1] < cavern_width:
                yield new_neighbour

def dijkstra(cavern, start):
    queue = []
    data = {}
    
    for row in range(len(cavern)):
        for col in range(len(cavern[0])):
            here = (row,col)
            data[here] = [float("inf"), None]
            if here == start:
                data[here][0] = 0
            
            heappush(queue, (data[here], here))

    while len(queue) > 0:
        _, node = heappop(queue)

        for neighbour in get_neighbours(cavern, node):
            alt = data[node][0] + cavern[neighbour[0]][neighbour[1]]
            if alt < data[neighbour][0]:
                data[neighbour][0] = alt
                data[neighbour][1] = node
                heapify(queue)
                # heapify is called here as you've modified the array in the dictionary,
                # but that's the same array that you put into the heapq, so you need to
                # ensure that the heapq is still correctly sorted

    return data

cavern = []

# with StringIO(test_cavern) as data:
with open("input15.txt") as data:
    for line in data:
        cavern.append([int(n) for n in line.strip()])
        
start = (0, 0) # row, column
target = (len(cavern)-1, len(cavern[0])-1)

begin = time()
results = dijkstra(cavern, start)
print(results[target][0])
print("duration:", time() - begin)