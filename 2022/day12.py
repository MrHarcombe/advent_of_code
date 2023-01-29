from io import StringIO
from collections import defaultdict
from heapq import *

heightmap = {}
start = None
starts = []
end = None

def get_neighbours(node):
    neighbours = []
    
    mx = max(heightmap.keys(), key=lambda i:i[0])[0]
    my = max(heightmap.keys(), key=lambda i:i[1])[1]
    
    # for delta in ((-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)):
    for delta in ((0,-1), (-1,0), (1,0), (0,1)):
        cx,cy = node
        dx,dy = delta
        cx += dx
        cy += dy
        if 0 <= cx <= mx and 0 <= cy <= my:
            # print(heightmap[(cx,cy)], "vs", heightmap[node])
            if heightmap[(cx,cy)] <= heightmap[node]+1:
                # neighbours.append(((cx,cy),1))
                neighbours.append((cx,cy))
        
    return neighbours

def astar_guess(node, goal):
    distance = sum(abs(val1-val2) for val1, val2 in zip(node, goal))
    return distance

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def a_star(start_node, end_node, func):
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
    g_score[start_node] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    f_score = defaultdict(lambda: float('inf'))
    f_score[start_node] = func(start_node, end_node)

    heappush(open_set, (f_score[start_node], start_node))

    while len(open_set) > 0:
        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        # current := the node in openSet having the lowest fScore[] value
        current = heappop(open_set)[1]

        # print('considering', current)
        if current == end_node:
            # print('at goal')
            return came_from

        for friend in get_neighbours(current):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_g_score = g_score[current] + 1 # g_score[current] + map[current[0]][current[1]]
            if tentative_g_score < g_score[friend]:
                # This path to neighbor is better than any previous one. Record it!
                came_from[friend] = current
                g_score[friend] = tentative_g_score
                friend_f_score = tentative_g_score + func(friend, end_node)
                f_score[friend] = friend_f_score
                if friend not in open_set:
                    heappush(open_set, (friend_f_score, friend))

    # Open set is empty but goal was never reached
    return


def dijkstra(start_node, end_node):
    queued = {n: [False, 0 if n == start_node else float("inf"), None] for n in heightmap.keys()}
    
    current_node = start_node
    while current_node != None:
        _, current_cost, _ = queued[current_node]
        for neighbour, cost in get_neighbours(current_node):
            visited, total_cost, _ = queued[neighbour]
            if not visited:
                if total_cost > current_cost + cost:
                    queued[neighbour][1] = current_cost + cost
                    queued[neighbour][2] = current_node

        queued[current_node][0] = True
        if end_node != None and current_node == end_node:
            current_node = None
        else:
            current_node, details = sorted(queued.items(), key=lambda n: (n[1][0], n[1][1]))[0]
            if queued[current_node][0]:
                current_node = None

    # print(queued)
    if end_node == None:
        return queued

    path = []
    try:
        current = end_node
        while current != start_node:
            path.append(current)
            current = queued[current][2]
        path.append(current)
        shortest = path[::-1]
        return shortest
    except KeyError:
        return []


def shortest_breadth_first(start_xy, end_xy):
    discovered = []
    queue = []

    discovered.append(start_xy)
    queue.append([start_xy])
    while len(queue) > 0:
        current_path = queue.pop(0)
        current_node = current_path[-1]

        # print("processing", current_node, hashkey)

        if current_node == end_xy:
            return current_path

        neighbours = get_neighbours(current_node)
        # print("neighbours:", neighbours)

        for neighbour in neighbours:
            if not neighbour in discovered:
                discovered.append(neighbour)
                new_path = list(current_path)
                new_path.append(neighbour)
                queue.append(new_path)

    return current_path



test = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

# with StringIO(test) as f:
with open("input12.txt") as f:
    for y, line in enumerate(f):
        for x, ch in enumerate(line.strip()):
            if ch == "S":
                start = (x,y)
                # starts.append((x,y))
                heightmap[(x,y)] = ord("a") - ord("a")
            elif ch == "E":
                end = (x,y)
                heightmap[(x,y)] = ord("z") - ord("a")
            else:
                if ch == "a":
                    starts.append((x,y))
                heightmap[(x,y)] = ord(ch) - ord("a")

    # path = shortest_breadth_first(start, end)
    # path = dijkstra(start, end)
    path = reconstruct_path(a_star(start, end, astar_guess), end)
    print("part 1:", len(path)-1)

    possibles = []
    for other in starts:
        path = a_star(other, end, astar_guess)
        if path != None:
            path = reconstruct_path(path, end)
            possibles.append(len(path)-1)
    print("part 2:", min(possibles))
