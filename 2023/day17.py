from collections import defaultdict
from structures import WeightedMatrixGraph
from heapq import heappop, heappush, heapify
from io import StringIO

test = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

test = """11599
99199
99199
99199
99111"""

def transform_city(city):
    new_city = WeightedMatrixGraph(True)

    # for row in range(city["max_row"]+1):
    #     for col in range(city["max_col"]+1):
    #         node = (row,col)
    #         new_city.add_node(node)
    #         for d, (dr, dc) in enumerate(((-1,0), (0,1), (1,0), (0,-1))):
    #             if 0 <= row+dr <= city["max_row"] and 0 <= col+dc <= city["max_col"]:
    #                 neighbour = (row + dr, col + dc)
    #                 new_city.add_node(neighbour)
    #                 new_city.add_edge(node, neighbour, city[neighbour])
    # 
    #                 cost = 0
    #                 for step in range(2, 4):
    #                     new_node = (row + dr * step, col + dc * step)
    #                     if 0 <= new_node[0] <= city["max_row"] and 0 <= new_node[1] <= city["max_col"]:
    #                         cost += city[new_node]
    #                         new_city.add_node((new_node,d,step))
    #                         new_city.add_edge(node, (new_node,d,step), cost)

    

    return new_city

def get_neighbours(graph, point, previous):
    for d, (dr, dc) in enumerate(((-1,0), (0,1), (1,0), (0,-1))):
        new_point = (point[0] + dr, point[1] + dc)
        if 0 <= new_point[0] <= graph["max_row"] and 0 <= new_point[1] <= graph["max_col"]:
            if len(previous) > 0:
                if previous[-1] == (d + 2) % 4:
                    # print(point, new_point, "not doubling back:", previous[-1], d)
                    continue

                most_recent = previous[-3:]
                if len(most_recent) == 3 and all(d == p for p in most_recent):
                    # print(point, new_point, "turning:", most_recent, d)
                    continue

            yield new_point, d

def a_star_guess(node, goal):
    # return the cityblock / manhattan distance
    return sum(abs(p1-p2) for p1, p2 in zip(node, goal))

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def cost(cavern, trace):
    total_cost = 0
    for step in trace[1:]:
        total_cost += cavern[step]
    return total_cost

def a_star(graph, start, goal, func):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    # openSet = {start}
    open_set = []

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    came_from = {}

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = func(start, goal)

    # For node n, bestPath[n] is the best path to the node discovered so far
    best_path = defaultdict(list)

    heappush(open_set, (f_score[start], start))

    while len(open_set) > 0:
        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        # current := the node in openSet having the lowest fScore[] value
        current = heappop(open_set)[1]

        if current == goal:
            return came_from

        for friend, dx in get_neighbours(graph, current, best_path[current]):
            # d(current, neighbour) is the weight of the edge from current to neighbour
            # tentative_gScore is the distance from start to the neighbour through current
            tentative_g_score = g_score[current] + graph[current]
            if tentative_g_score < g_score[friend]:
                # This path to neighbour is better than any previous one. Record it!
                came_from[friend] = current
                g_score[friend] = tentative_g_score
                friend_f_score = tentative_g_score + func(friend, goal)
                f_score[friend] = friend_f_score
                best_path[friend] = list(best_path[current]) + [dx]
                if friend not in open_set:
                    heappush(open_set, (friend_f_score, friend))

    # Open set is empty but goal was never reached
    return

def dijkstra(graph, start, end):
    queue = []
    data = {}
    
    for row in range(graph["max_row"]+1):
        for col in range(graph["max_col"]+1):
            spot = (row,col)
            data[spot] = [float("inf"), None, []]
            if spot == start:
                data[spot][0] = 0

            heappush(queue, (data[spot], spot))

    while len(queue) > 0:
        _, node = heappop(queue)
        node_path = data[node][2]

        for neighbour, direction in get_neighbours(graph, node, node_path):
            cost = data[node][0] + graph[neighbour]
            if cost < data[neighbour][0]:
                data[neighbour][0] = cost
                data[neighbour][1] = node
                data[neighbour][2] = list(node_path) + [direction]
                heapify(queue)
                # heapify is called here as you've modified the array in the dictionary,
                # but that's the same array that you put into the heapq, so you need to
                # ensure that the heapq is still correctly sorted

    if end == None:
        return data

    path = []
    current = end
    while current != start:
        path.append(current)
        current = data[current][1]
    path.append(current)
    shortest = path[::-1]
    return shortest, data

city = {}
with StringIO(test) as data:
# with open("input17.txt") as data:
    for row, line in enumerate(data):
        for col, ch in enumerate(line.strip()):
            city[(row,col)] = int(ch)

city["max_row"] = row
city["max_col"] = col

start=(0,0)
end=(row,col)

expanded = transform_city(city)
path = expanded.dijkstra(start, end)
print(path[0])
for p in path[1:]:
    print(f"{p} ({city[p]})")
print("Part 1:", sum(city[p] for p in path[1:]))

# path, workings = dijkstra(city, start, end)
# print("Part 1:", sum(city[p] for p in path[1:]))

# path = reconstruct_path(a_star(city, start, end, a_star_guess), end)
# if path:
#     print("Part 1:", cost(city, path))
