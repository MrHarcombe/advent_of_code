from io import StringIO
from structures import MatrixGraph

test = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

pipe_map = MatrixGraph(True)

# with StringIO(test) as data:
with open("input12.txt") as data:
    for line in data:
        source, dest_list = line.strip().split("<->")
        dests = dest_list.split(",")

        for dest in dests:
            pipe_map.add_edge(source.strip(), dest.strip())

# print(pipe_map.matrix[0])
grouped = set(pipe_map.breadth_first("0"))
print("Part 1:", len(grouped), "->", pipe_map.breadth_first("0"))

group_count = 1
for pipe in pipe_map.matrix[0]:
    if pipe not in grouped:
        grouping = set(pipe_map.breadth_first(pipe))
        grouped |= grouping
        group_count += 1
        
print("Part 2:", group_count)