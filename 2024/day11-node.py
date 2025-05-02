from io import StringIO
from math import log10, ceil
from time import time

test = """0 1 10 99 999"""
test = "125 17"


class Node:
    stones = 0

    def __init__(self, value):
        self.value = value
        self.next = None
        Node.stones += 1


# with StringIO(test) as input_data:
with open("input11.txt") as input_data:
    for line in input_data:
        stones = map(int, line.strip().split())

begin = time()

head_stone = Node(next(stones))
while head_stone is not None:
    for step in range(75):
        print(f"Step {step+1}")
        current = head_stone
        while current is not None:
            stone = current.value
            if stone == 0:
                current.value = 1
                current = current.next
            elif log10(stone) > 0 and ceil(log10(stone)) % 2 == 0:
                mid = ceil(log10(stone)) // 2
                current.value = stone // 10**mid
                new = Node(stone % 10**mid)
                new.next = current.next
                current.next = new
                current = new.next
            else:
                current.value = stone * 2024
                current = current.next

        # print(f"{step+1}:", stones)
        # print("Stones:", Node.stones)
        # print("Elapsed:", time() - begin)

    next_stone = next(stones, None)
    if next_stone is not None:
        head_stone = Node(next_stone)
    else:
        head_stone = None

# count = 0
# runner = head
# while runner is not None:
#     count += 1
#     runner = runner.next
print("Stones:", Node.stones)
print("Elapsed:", time() - begin)
