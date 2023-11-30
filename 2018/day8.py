from io import StringIO

test = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"""

class node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata
        
    def traverse_sum(self):
        total = sum(self.metadata)
        for ch in self.children:
            total += ch.traverse_sum()
        return total
    
    def value(self):
        if len(self.children) == 0:
            return sum(self.metadata)
        else:
            value = 0
            for m in self.metadata:
                if m-1 in range(len(self.children)):
                    value += self.children[m-1].value()
            return value

def parse_node(tokens):
    num_ch = tokens.pop(0)
    num_m = tokens.pop(0)
    children = []
    for ch in range(num_ch):
        children.append(parse_node(tokens))
    metadata = []
    for meta in range(num_m):
        metadata.append(tokens.pop(0))
    return node(children, metadata)

# with StringIO(test) as data:
with open("input8.txt") as data:
    for line in data:
        license = list(map(int, line.strip().split()))
    # print(license)
    
root = parse_node(license)
print("Part 1:", root.traverse_sum())
print("Part 2:", root.value())
