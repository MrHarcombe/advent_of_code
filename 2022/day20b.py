from io import StringIO

class Node:
    def __init__(self, order, value):
        self.order = order
        self.value = value
        self.next = self
        self.previous = self
        
    def insert_before(self, node):
        runner = node
        while runner.next != node:
            runner = runner.next
        
        self.previous = runner
        runner.next = self
        self.next = node
        node.previous = self
        
    def insert_after(self, node):
        runner = node
        while runner.next != node:
            runner = runner.next
            
        self.next = runner
        node.previous = self
        self.previous = node
        node.next = self
        
    def move_right(self):
        current_next = self.next
        current_previous = self.previous

        self.previous = current_next
        self.next = current_next.next
        self.next.previous = self

        current_previous.next = current_next
        current_next.previous = current_previous
        current_next.next = self
        
    def move_left(self):
        current_next = self.next
        current_previous = self.previous

        self.next = current_previous
        self.previous = current_previous.previous
        self.previous.next = self

        current_next.previous = current_previous
        current_previous.next = current_next
        current_previous.previous = self

    def __str__(self):
        output = f"{self.value}"
        runner = self
        while runner.next != self:
            runner = runner.next
            output += f", {runner.value}"

        return output

test = """0
-1
-1
1"""

test = """1
2
-3
3
-2
0
4"""

order = 0
nodes = None
values = []

# with StringIO(test) as f:
with open("input20.txt") as f:
    for line in f:
        # node = Node(order, int(line.strip()))
        # if nodes == None:
        #     nodes = node
        # else:
        #     node.insert_before(nodes)
        values.append((order, int(line.strip()) * 811589153))
        # values.append((order, int(line.strip())))
        order += 1

for i in range(10):
    for o in range(order):
        current = next((index for index, value in enumerate(values) if value[0] == o), None)
        value = values[current][1]
        new = current + value
        del values[current]

        # while new <= 0:
        #     new += len(values)
        if new <= 0:
            new = new % len(values)

        # while new >= len(values):
        #     new -= len(values)
        if new >= len(values):
            new = new % len(values)

        values.insert(new, (o, value))
        # print(value, "->", values)
    # print("\n###\n")

# for value in order:
#     current = values.index(value)
#     swaps = abs(values[current])
#     pos = current
#     while swaps > 0:
#         if value < 0:
#             pos_next = pos - 1
#             if pos_next < 0: pos_next == len(values) - 1
#             values[pos], values[pos_next] = values[pos_next], values[pos]
#             pos -= 1
#             if pos < 0: pos = len(values) - 1
#         else:
#             pos_next = pos + 1
#             if pos_next >= len(values): pos_next = 0
#             values[pos], values[pos_next] = values[pos_next], values[pos]
#             pos += 1
#             if pos >= len(values): pos = 0
#         swaps -= 1
#     print(value, "->", values)

# for o in range(order):
#     runner = nodes
#     while runner.order != o:
#         runner = runner.next
# 
#     swaps = abs(runner.value)
#     for swap in range(swaps):
#         if runner.value < 0:
#             runner.move_left()
#         else:
#             runner.move_right()
# 
#     # print(runner.value, "->", nodes)
# 
# zero = nodes
# while zero.value != 0:
#     zero = zero.next
# 
# first = 1000 % order
# second = 2000 % order
# third = 3000 % order
# 
# runner = zero
# for i in range(1000):
#     runner = runner.next
# first = runner.value
# 
# for i in range(1000):
#     runner = runner.next
# second = runner.value
# 
# for i in range(1000):
#     runner = runner.next
# third = runner.value
# 
# print(first+second+third)

zero = next((index for index, value in enumerate(values) if value[1] == 0), None)
first = (zero + 1000) % order
second = (zero + 2000) % order
third = (zero + 3000) % order

# print(zero, first, second, third)
print(values[first][1] + values[second][1] + values[third][1])
