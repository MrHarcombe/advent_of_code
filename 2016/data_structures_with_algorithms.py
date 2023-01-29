class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def append_left(self, left):
        self.left = left

    def append_right(self, right):
        self.right = right

    def pre_traverse(self, op):
        op(self.value)
        if self.left != None:
            self.left.pre_traverse(op)
        if self.right != None:
            self.right.pre_traverse(op)

    def in_traverse(self, op):
        if self.left != None:
            self.left.in_traverse(op)
        op(self.value)
        if self.right != None:
            self.right.in_traverse(op)

    def post_traverse(self, op):
        if self.left != None:
            self.left.post_traverse(op)
        if self.right != None:
            self.right.post_traverse(op)
        op(self.value)

    def __str__(self):
        return f"TreeNode({self.value}, {'NoLeft' if self.left == None else 'HasLeft'}, {'NoRight' if self.right == None else 'HasRight'})"


class Tree:
    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root == None

    def add(self, value):
        if self.is_empty():
            self.root = TreeNode(value)

        else:
            new_node = TreeNode(value)

            current = self.root
            looking = True
            while looking:
                if value < current.value:
                    if current.left == None:
                        current.append_left(new_node)
                        looking = False
                    else:
                        current = current.left

                else:
                    if current.right == None:
                        current.append_right(new_node)
                        looking = False
                    else:
                        current = current.right

    def contains(self, value):
        return value in self

    def __contains__(self, value):
        found = False
        
        if not self.is_empty():
            current = self.root
            looking = True
            while looking:
                if value == current.value:
                    found = True
                    looking = False
                
                elif value < current.value:
                    if current.left == None:
                        looking = False
                    else:
                        current = current.left
                
                else:
                    if current.right == None:
                        looking = False
                    else:
                        current = current.right

        return found

    def pre_traverse(self, op):
        if not self.is_empty():
            self.root.pre_traverse(op)

    def in_traverse(self, op):
        if not self.is_empty():
            self.root.in_traverse(op)

    def post_traverse(self, op):
        if not self.is_empty():
            self.root.post_traverse(op)


class ListGraph:
    class ListGraphNode:
        def __init__(self, node):
            self.node = node
            self.paths = []

        def add_edge(self, to):
            if to not in self.paths:
                self.paths.append(to)

        def is_connected(self, to):
            return to in self.paths

        def __str__(self):
            return f"ListGraphNode(node: {self.node}, paths: {', '.join(self.paths)})"


    def __init__(self):
        self.nodes = []

    def contains(self, value):
        return value in self

    def __contains__(self, value):
        for n in self.nodes:
            if n.node == value:
                return True
        return False

    def add_node(self, node):
        if not node in self:
            self.nodes.append(ListGraph.ListGraphNode(node))

    def delete_node(self, node):
        if node in self:
            # remove the node itself
            for n in range(len(self.nodes)):
                if self.nodes[n].node == node:
                    break
            del self.nodes[n]
            # remove references to the node
            for n in self.nodes:
                if node in n.paths:
                    n.paths.remove(node)

    def add_edge(self, from_node, to_node):
        if from_node in self and to_node in self:
            for n in self.nodes:
                if n.node == from_node:
                    n.add_edge(to_node)
                elif n.node == to_node:
                    n.add_edge(from_node)

    def is_connected(self, from_node, to_node):
        if from_node in self and to_node in self:
            for n in self.nodes:
                if n.node == from_node:
                    return n.is_connected(to_node)
        return False


class MatrixGraph:
    def __init__(self):
        self.matrix = [[]]
    
    def is_empty(self):
        return len(self.matrix[0] == 0)

    def contains(self, node):
        return node in self.matrix[0]

    def __contains__(self, node):
        return self.contains(node)
    
    def add_node(self, node):
        if not node in self.matrix[0]:
            self.matrix[0].append(node)
            for n in range(1, len(self.matrix)):
                self.matrix[n].append(False)
            self.matrix.append([False for n in range(len(self.matrix[0]))])

    def delete_node(self, node):
        if node in self.matrix[0]:
            index = self.matrix[0].index(node)
            del self.matrix[0][index]
            del self.matrix[index]
            for n in range(1, len(self.matrix)):
                del self.matrix[n][index]

    def add_edge(self, from_node, to_node):
        if from_node in self.matrix[0] and to_node in self.matrix[0] and not self.is_connected(from_node, to_node):
            from_index = self.matrix[0].index(from_node)
            to_index = self.matrix[0].index(to_node)
            self.matrix[from_index+1][to_index] = True
            self.matrix[to_index+1][from_index] = True

    def is_connected(self, from_node, to_node):
        if from_node in self.matrix[0] and to_node in self.matrix[0]:
            from_index = self.matrix[0].index(from_node)
            to_index = self.matrix[0].index(to_node)
            return self.matrix[to_index+1][from_index]
        return False


class WeightedMatrixGraph:
    """ a weighted, directional graph """
    def __init__(self, undirected=False):
        self.matrix = [[]]
        self.undirected = undirected
    
    def is_empty(self):
        return len(self.matrix[0] == 0)

    def contains(self, node):
        return node in self.matrix[0]

    def __contains__(self, node):
        return self.contains(node)
    
    def add_node(self, node):
        if not node in self.matrix[0]:
            self.matrix[0].append(node)
            for n in range(1, len(self.matrix)):
                self.matrix[n].append(None)
            self.matrix.append([None for n in range(len(self.matrix[0]))])

    def delete_node(self, node):
        if node in self.matrix[0]:
            index = self.matrix[0].index(node)
            del self.matrix[0][index]
            del self.matrix[index]
            for n in range(1, len(self.matrix)):
                del self.matrix[n][index]

    def add_edge(self, from_node, to_node, weight=1, undirected=False):
        if from_node in self.matrix[0] and to_node in self.matrix[0]:
            from_index = self.matrix[0].index(from_node)
            to_index = self.matrix[0].index(to_node)
            self.matrix[from_index+1][to_index] = weight
            if self.undirected or undirected:
                self.matrix[to_index+1][from_index] = weight

    def is_connected(self, from_node, to_node):
        if from_node in self.matrix[0] and to_node in self.matrix[0]:
            from_index = self.matrix[0].index(from_node)
            to_index = self.matrix[0].index(to_node)
            return self.matrix[from_index+1][to_index]
        return None

    def get_connections(self, node):
        if node in self.matrix[0]:
            return iter([c for c in zip(self.matrix[0], self.matrix[self.matrix[0].index(node)+1]) if c[1] != None])
        return []

    def depth_first(self, start_node):
        if start_node in self.matrix[0]:
            discovered = []
            visited = []
            stack = []

            discovered.append(start_node)
            stack.append(start_node)
            while len(stack) > 0:
                current = stack.pop()
                visited.append(current)

                for node, weight in self.get_connections(current):
                    if not node in discovered:
                        discovered.append(node)
                        stack.append(node)
            return visited
        return None

    def breadth_first(self, start_node):
        if start_node in self.matrix[0]:
            discovered = []
            visited = []
            queue = []

            discovered.append(start_node)
            queue.append(start_node)
            while len(queue) > 0:
                current = queue.pop(0)
                visited.append(current)

                for node, weight in self.get_connections(current):
                    if not node in discovered:
                        discovered.append(node)
                        queue.append(node)
            return visited
        return None

    def dijkstra(self, start_node, end_node=None):
        queued = {n: [False, 0 if n == start_node else float("inf"), None] for n in self.matrix[0]}
        
        current_node = start_node
        while current_node != None:
            _, current_cost, _ = queued[current_node]
            for neighbour, cost in self.get_connections(current_node):
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
        current = end_node
        while current != start_node:
            path.append(current)
            current = queued[current][2]
        path.append(current)
        shortest = path[::-1]
        return shortest


if __name__ == "__main__":
    def test_tree():
        print("Testing tree...")
        t = Tree()
        for n in (7, 4, 2, 6, 16, 12, 19):
            t.add(n)
        print(12 in t)
        print(13 in t)
        t.add(10)
        print(10 in t)

        tree = []
        print("Pre-order traversal:")
        t.pre_traverse(lambda value : tree.append(str(value)))
        print(", ".join(tree))

        tree = []
        print("In-order traversal:")
        t.in_traverse(lambda value : tree.append(str(value)))
        print(", ".join(tree))

        tree = []
        print("Post-order traversal:")
        t.post_traverse(lambda value : tree.append(str(value)))
        print(", ".join(tree))
        print("...done")

    def test_list_graph():
        print("Testing graph (adjacency list)...")
        g = ListGraph()
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "C")
        print("B" in g)
        print(g.is_connected("A", "B"))
        print(g.is_connected("A", "C"))
        g.add_node("D")
        g.add_edge("B", "D")
        g.add_edge("C", "D")
        g.delete_node("C")
        print("D" in g)
        print("C" in g)
        print(g.is_connected("A", "C"))
        print(g.is_connected("B", "D"))
        print("...done")

    def test_matrix_graph():
        print("Testing graph (adjacency matrix)...")
        g = MatrixGraph()
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        g.add_edge("B", "C")
        print("B" in g)
        print(g.is_connected("A", "B"))
        print(g.is_connected("A", "C"))
        g.add_node("D")
        g.add_edge("B", "D")
        g.add_edge("C", "D")
        g.delete_node("C")
        print("D" in g)
        print("C" in g)
        print(g.is_connected("A", "C"))
        print(g.is_connected("B", "D"))
        print("...done")

    def test_weighted_graph():
        print("Testing graph (adjacency matrix)...")
        g = WeightedMatrixGraph(True)
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_node("D")
        g.add_edge("A", "B", 2)
        g.add_edge("A", "C", 10)
        g.add_edge("B", "D", 3)
        g.add_edge("C", "D", 6)
        print("C" in g)
        print(g.is_connected("A", "C"))
        print(g.is_connected("B", "D"))
        g.add_node("E")
        g.add_node("F")
        g.add_node("G")
        g.add_node("H")
        g.add_edge("B", "E", 9)
        g.add_edge("D", "F", 11)
        g.add_edge("D", "G", 7)
        g.add_edge("C", "G", 8)
        g.add_edge("E", "F", 5)
        g.add_edge("F", "H", 6)
        g.add_edge("G", "H", 1)
        print("D" in g)
        print(g.is_connected("D", "F"))

        visited = g.depth_first("A")
        print("depth first from A: ", ",".join(visited))

        visited = g.breadth_first("A")
        print("breadth first from A: ", ",".join(visited))

        print("shortest path from A:", g.dijkstra("A"))
        print("shortest path from A to H:", ",".join(g.dijkstra("A", "H")))
        print("shortest path from F to C:", ",".join(g.dijkstra("F", "C")))

        print("...done")

    def test_graph_connections():
        g = WeightedMatrixGraph()
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_node("D")
        g.add_edge("A", "B")
        g.add_edge("A", "C")
        for e in g.get_connections("A"):
            print("Connected to", e)
        print(g.matrix)
    
    test_weighted_graph()