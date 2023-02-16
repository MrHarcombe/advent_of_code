from math import copysign

###
#
# Hex board (see http://althenia.net/svn/stackoverflow/hexgrid.png)
#
# Can be either horizontally or vertically offset (see below) but in both
# cases, the y-axis is offset to the x-axis by 60 degrees (not 90)
#
# Movement from a location is done by compass point, location is stored
# internally to the grid
#
#        _____                     /\  /\
#  _____/ 0,1 \_____              /-1\/ 0\
# /-1,1 \_____/ 1,0 \            | , | , |
# \_____/ 0,0 \_____/            /\ 1/\ 1/\
# /-1,0 \_____/ 1,-1\           /-1\/0 \/1 \
# \_____/ 0,-1\_____/          | , | , | , |
#       \_____/                 \0 /\0 /\0 /
#                                \/ 0\/ 1\/
#                                | , | , |
#                                 \-1/\-1/
#                                  \/  \/
#

class HexGrid:
    @staticmethod
    def get_origin():
        return (0,0)

    @staticmethod
    def distance(key1, key2):
        x0, y0 = key1
        x1, y1 = key2
        
        dx = x1 - x0
        dy = y1 - y0

        if copysign(dx, dy) == dx:
            return abs(dx + dy)
        else:
            return max(abs(dx), abs(dy))

    def __init__(self, horiz=True):
        self.__horizontal_offset = horiz
        self.__board = {}

    def __len__(self):
        return len(self.__board)

    def __getitem__(self, key):
        return self.__board[key]

    def __setitem__(self, key, value):
        self.__board[key] = value

    def __delitem__(self, key):
        del self.__board[key]

    def __iter__(self):
        return iter(self.__board)

    def __contains__(self, key):
        return key in self.__board

    def keys(self):
        return iter(self.__board)
    
    def items(self):
        return self.__board.items()
    
    def values(self):
        return self.__board.values()

    def get(self, key, default=None):
        return self.__board.get(key, default)

    def get_neighbour(self, key, direction):
        dx, dy = 0, 0

        if self.__horizontal_offset:
            match direction.lower():
                case "nw":
                    dx = -1
                    dy = 1
                case "n":
                    dy = 1
                case "ne":
                    dx = 1
                case "se":
                    dx = 1
                    dy = -1
                case "s":
                    dy = -1
                case "sw":
                    dx = -1
        else:
            match direction.lower():
                case "w":
                    dx = -1
                case "nw":
                    dx = -1
                    dy = 1
                case "ne":
                    dy = 1
                case "e":
                    dx = 1
                case "se":
                    dx = 1
                    dy = -1
                case "sw":
                    dy = -1

        return (key[0]+dx, key[1]+dy)

    def get_neighbours(self, key):
        if self.__horizontal_offset:
            neighbours = ((-1,1), (0,1), (1,0), (1,-1), (0,-1), (-1,0))
        else:
            neighbours = ((-1,1), (0,1), (1,0), (1,-1), (0,-1), (-1,0))

        for dx, dy in neighbours:
                yield (key[0] + dx, key[1] + dy)

    def dijkstra(self, start, end=None):
        queued = {n: [False, 0 if n == start else float("inf"), None] for n in self.__board}
        
        current_cell = start
        while current_cell != None:
            _, current_cost, _ = queued[current_cell]
            for neighbour in self.get_neighbours(current_cell):
                visited, total_cost, _ = queued[neighbour]
                if not visited:
                    if total_cost > current_cell + 1:
                        queued[neighbour][1] = current_cell + 1
                        queued[neighbour][2] = current_node

            queued[current_cell][0] = True
            if end_node != None and current_node == end_node:
                current_cell = None
            else:
                current_cell, details = sorted(queued.items(), key=lambda n: (n[1][0], n[1][1]))[0]
                if queued[current_cell][0]:
                    current_cell = None

        # print(queued)
        if end_node == None:
            return queued

        path = []
        current = end
        while current != start:
            path.append(current)
            current = queued[current][2]
        path.append(current)
        shortest = path[::-1]
        return shortest


if __name__ == "__main__":
    board = HexGrid(True)
    origin = HexGrid.get_origin()
    board[origin] = 1
    board[board.get_neighbour(origin, "nw")] = 1
    
    for h in board.keys():
        print("key:", h)
        for n in board.get_neighbours(h):
            print(n, n in board)
