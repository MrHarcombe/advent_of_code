from io import StringIO
from operator import add, mul

test = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

class Monkey:
    def __init__(self, number, items, worry, test, true, false):
        self.number = number
        self.items = items
        self.worry = self.__define_worry(worry)
        self.test = test
        self.true = true
        self.false = false

    def inspect_items(self):
        while len(self.items) > 0:
            yield self.items.pop(0)

    def inspect(self, item):
        # print("#",self.number,item)
        item = self.worry(item)
        # print("up to", item)
        # item = item//3
        # print("down to", item)
        if item % self.test == 0:
            # print("throwing to", self.true)
            monkeys[self.true][0].catch(item)
        else:
            # print("throwing to", self.false)
            monkeys[self.false][0].catch(item)

    def catch(self, item):
        self.items.append(item)

    def __define_worry(self, worry):
        operator = add if worry[0] == "+" else mul
        amount = int(worry[1]) if worry[1].isdigit() else None
        
        return lambda i : operator(i, i if amount == None else amount)
        
    def __repr__(self):
        return f"M(#:{self.number}, has:{self.items})"

monkeys = {}

with StringIO(test) as f:
# with open("input11.txt") as f:
    for line in f:
        if line.startswith("Monkey"):
            number = int(line.split()[1][:-1])
            items = [int(n) for n in f.readline().split(":")[1].split(",")]
            worry = f.readline().split("=")[1].strip().split()[1:]
            test = int(f.readline().split()[-1])
            true = int(f.readline().split()[-1])
            false = int(f.readline().split()[-1])
        
            monkeys[number] = [Monkey(number, items, worry, test, true, false), 0]

    # for t in range(20):
    for t in range(10000):
        for m in range(max(monkeys)+1):
            # print("Turn:", t+1, "monkey:", m)
            for item in monkeys[m][0].inspect_items():
                monkeys[m][0].inspect(item)
                monkeys[m][1] += 1

    print(mul(*sorted([v[1] for v in monkeys.values()])[-2:]))

