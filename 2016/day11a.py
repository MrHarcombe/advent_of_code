from data_structures_with_algorithms import WeightedMatrixGraph
from io import StringIO
from itertools import combinations
from string import ascii_uppercase

test1 = """The first floor contains a hydrogen-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains nothing relevant.
The fourth floor contains nothing relevant."""
test2 = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""
test = test2

floor_numbers = { "first" : 0, "second" : 1, "third" : 2, "fourth" : 3 }

def parse_floor_map(floors, floor, contents):
    # print(floor, contents)
    floor_number = floor_numbers[floor]
    if "nothing" in contents:
        pass
    else:
        before, *after = contents.split("and")
        multiple = before.split(",") + after
        # print(multiple)
        for component in multiple:
            parts = component.split()
            if len(parts) > 1:
                element = parts[1].split("-")[0]
                part = parts[2].split(".")[0]
                # print(element, part)
                floors[f"{element}-{part[0]}"] = floor_number
                
    return floors

def is_valid(floors, current_floor):
    items = [item for item, floor in floors.items() if floor == current_floor]
    active = False
    chips = set()
    generators = set()
    for item in items:
        if item.endswith("-m"):
            if item[:-2] + "-g" in generators:
                active = True
            else:
                chips.add(item)
        else:
            if item[:-2] + "-m" in chips:
                active = True
                chips.discard(item[:-2] + "-m")
            else:
                generators.add(item)

    # print("active:", active, "chips:", chips, "generators:", generators)
    return not active or (active and len(chips) == 0)

def generate_node_name(node, current_floor):
    # make into a generic node name, ordered by floor
    parts = []
    seen = {}
    next_letter = 0
    for item, floor in sorted(node.items(), key=lambda item: item[1]):
        if item[:-2] not in seen:
            seen[item[:-2]] = ascii_uppercase[next_letter]
            next_letter += 1

        parts.append((seen[item[:-2]] + item[-1:], floor))

    node_name = "".join([f"{item}{floor}" for item, floor in sorted(parts)]) + f"@{current_floor}"
    return node_name

    # return a specific node name    
    # return "/".join([f"{item[0]}-{item[1]}" for item in node.items()]) + f"@{current_floor}"

def generate_paths_recursive(floors, graph, visited={}, current_floor=0, previous_name=""):
    print(floors, len(graph.matrix[0]), current_floor, previous_name, generate_node_name(floors) not in graph, is_valid(floors, current_floor))

    name = generate_node_name(floors)
    if name not in graph:
        graph.add_node(name)
        visited[name] = False
        if previous_name:
            graph.add_edge(name, previous_name)

    if is_valid(floors, current_floor) and not visited[name]:
        current_items = [item for item, floor in floors.items() if floor == current_floor]
        visited[name] = True
        for item in current_items + list(combinations(current_items, min(2, len(current_items)))):
            # print(item)
            if current_floor < 3:
                up = current_floor + 1
                if isinstance(item, str):
                    #print("up", item, current_floor, up)
                    generate_paths(floors | {item:up}, graph, visited, up, name)
                elif len(item) > 1:
                    #print("up", item[0], item[1], current_floor, up)
                    generate_paths(floors | {item[0]:up, item[1]:up}, graph, visited, up, name)
            if current_floor > 0:
                down = current_floor - 1
                if isinstance(item, str):
                    #print("down", item, current_floor, down)
                    generate_paths(floors | {item:down}, graph, visited, down, name)
                elif len(item) > 1:
                    #print("down", item[0], item[1], current_floor, down)
                    generate_paths(floors | {item[0]:down, item[1]:down}, graph, visited, down, name)

def generate_paths(floors, graph):
    queue = []
    visited = []

    start_node = generate_node_name(floors, 0)

    graph.add_node(start_node)
    queue.append((start_node, floors, 0))
    
    while len(queue) > 0:
        current_node, current_floors, current_floor = queue.pop(0)
        if current_node not in visited:
            print("processing", current_node, f"({len(graph.matrix[0])})")
            graph.add_node(current_node)
            
            current_items = [item for item, floor in current_floors.items() if floor == current_floor]
            paired_items = list(combinations(current_items, min(2, len(current_items))))
                
            if current_floor < 3:
                up = current_floor + 1

                # from reddit hints - move two items at a time, if possible...
                valid_pair = False
                if len(current_items) > 1:
                    for item in paired_items:
                        #print("up", item[0], item[1], current_floor, up)
                        new_floors = current_floors | {item[0]:up, item[1]:up}
                        new_node = generate_node_name(new_floors, up)
                        
                        if is_valid(new_floors, up):
                            valid_pair = True
                            graph.add_node(new_node)
                            graph.add_edge(current_node, new_node)
                        #else:
                        #    graph.add_edge(current_node, new_node, float("inf"))
                        
                        queue.append((new_node, new_floors, up))

                # ...failing that, move just the one
                if not valid_pair:
                    for item in current_items:
                        #print("up", item, current_floor, up)
                        new_floors = current_floors | {item:up}
                        new_node = generate_node_name(new_floors, up)
                        
                        if is_valid(new_floors, up):
                            graph.add_node(new_node)
                            graph.add_edge(current_node, new_node)
                        #else:
                        #    graph.add_edge(current_node, new_node, float("inf"))
                        
                        queue.append((new_node, new_floors, up))


            # from reddit hints - don't move anything back down if all floors lower are empty
            if current_floor > 0 and len([item for item, floor in current_floors.items() if floor < current_floor]) > 0:
                down = current_floor - 1
                
                # from reddit hints - move one item down if there are any items available...
                if len(current_items) > 0:
                    for item in current_items:
                        #print("down", item, current_floor, down)
                        new_floors = current_floors | {item:down}
                        new_node = generate_node_name(new_floors, down)
                        
                        if is_valid(new_floors, down):
                            graph.add_node(new_node)
                            graph.add_edge(current_node, new_node)
                        #else:
                        #    graph.add_edge(current_node, new_node, float("inf"))
                        
                        queue.append((new_node, new_floors, down))

                # only move two items downstairs rarely
                elif len(item) > 1:
                    for item in paired_items:
                        #print("down", item[0], item[1], current_floor, down)
                        new_floors = current_floors | {item[0]:down, item[1]:down}
                        new_node = generate_node_name(new_floors, down)
                        
                        if is_valid(new_floors, down):
                            graph.add_node(new_node)
                            graph.add_edge(current_node, new_node)
                        #else:
                        #    graph.add_edge(current_node, new_node, float("inf"))

                        queue.append((new_node, new_floors, down))

            visited.append(current_node)


#with StringIO(test) as f:
with open("input11.txt") as f:
    floors = {}
    for line in f:
        _, floor, _, _, *contents = line.strip().split()
        parse_floor_map(floors, floor, " ".join(contents))
    #print(floors)
    
    graph = WeightedMatrixGraph(True)
    generate_paths(floors, graph)
    print(len(graph.matrix[0]))
    path = graph.dijkstra(generate_node_name(floors, 0), generate_node_name({k: 3 for k, v in floors.items()}, 3))
    print(path)
    print(len(path)-1)
