from io import StringIO
from operator import add, mul, sub, floordiv, eq

inverse = { add : sub, sub : add, mul : floordiv, floordiv : mul }

class Node:
    def __init__(self, name, value=None, left=None, right=None):
        self.name = name
        self.value = value
        if left != None:
            self.left = Node(left)
        else:
            self.left = None
        if right != None:
            self.right = Node(right)
        else:
            self.right = None

    def update(self, value, left=None, right=None):
        self.value = value
        if left != None:
            self.left = Node(left)
        else:
            self.left = None
        if right != None:
            self.right = Node(right)
        else:
            self.right = None

    def inorder_search(self, name):
        if self.left != None:
            found = self.left.inorder_search(name)
            if found != None:
                return found
        if self.name == name:
            return self
        if self.right != None:
            found = self.right.inorder_search(name)
            if found != None:
                return found

    def postorder_process(self):
        if isinstance(self.value, int):
            self.result = self.value
        else:
            if self.left != None:
                self.left.postorder_process()
                left = self.left.result
            if self.right != None:
                self.right.postorder_process()
                right = self.right.result
            if self.name == "root":
                print(left, right)
            self.result = self.value(left, right)            

    def preorder_process(self, avoid, total):
        if self.name == "humn":
            return total

        if self.left != None:
            found = self.left.inorder_search(avoid)

        if found == None:
            self.left.postorder_process()
            value = self.left.result
            
            if self.value in (add, mul):
                total = inverse[self.value](total, value)
            else:
                total = self.value(value, total)
            total = self.right.preorder_process(avoid, total)

        else:
            self.right.postorder_process()
            value = self.right.result
            total = inverse[self.value](total, value)
            total = self.left.preorder_process(avoid, total)

        return total

    def __str__(self):
        output = []
        
        if self.left != None:
            output.append(str(self.left))
        output.append(f"{self.value if self.name != 'humn' else '???'}")
        if self.right != None:
            output.append(str(self.right))

        return "(" + ",".join(output) + ")"

class Tree:
    def __init__(self, value, left=None, right=None):
        self.root = Node("root", value, left, right)
        # self.root = Node("root", eq, left, right)

    def expand(self, name, value, left=None, right=None):
        next_node = self.root.inorder_search(name)
        next_node.update(value, left, right)

    def part1(self):
        self.root.postorder_process()
        print(self.root.result)

    def part2(self):
        humn = self.root.left.inorder_search("humn")
        if humn == None:
            self.root.left.postorder_process()
            value = self.root.left.result
            calc = str(self.root.right)
            print(value, calc)
            result = self.root.right.preorder_process("humn", value)
            print(result)
        else:
            self.root.right.postorder_process()
            value = self.root.right.result
            calc = str(self.root.left)
            print(value, calc)
            result = self.root.left.preorder_process("humn", value)
            print(result)

    def __str__(self):
        return "Tree {" + str(self.root) + "}"

test = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

# test = """root: juli + josi
# juli: amee + alex
# amee: buki * abby
# buki: 5
# abby: 4
# alex: 4
# josi: benj / mark
# benj: 360
# mark: emly - humn
# emly: 34
# humn: 0"""

monkeys = {}
# with StringIO(test) as f:
with open("input21.txt") as f:
    for line in f:
        monkey, job = line.strip().split(":")
        # if monkey == "humn":
        #     # job = 7650891667780.364
        #     job = 960.005
        #     monkeys[monkey] = job
        # elif job.strip().isdigit():
        if job.strip().isdigit():
            job = int(job)
            monkeys[monkey] = job
        else:
            left, op, right = job.split()
            if op == "+": op = add
            elif op == "-": op = sub
            elif op == "*": op = mul
            elif op == "/": op = floordiv
            monkeys[monkey] = (op, left, right)

op, left, right = monkeys["root"]
tree = Tree(op, left, right)
queue = [left, right]
while len(queue) > 0:
    name = queue.pop()
    if isinstance(monkeys[name],int):
        value = monkeys[name]
        tree.expand(name, value)
    else:
        op, left, right = monkeys[name]
        tree.expand(name, op, left, right)
        queue.append(left)
        queue.append(right)

# tree.part1()
tree.part2()