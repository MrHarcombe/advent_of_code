#!/bin/python3
import collections

#ELF_COUNT = 3014604
ELF_COUNT = 10

def solve_parttwo():
    left = collections.deque([n for n in range(1, (ELF_COUNT // 2) + 1)])
    right = collections.deque([n for n in range(ELF_COUNT, (ELF_COUNT // 2), -1)])

#     for i in range(1, ELF_COUNT+1):
#         if i < (ELF_COUNT // 2) + 1:
#             left.append(i)
#         else:
#             right.appendleft(i)

    print(left, right)

    while left and right:
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()

        print(left, right)

        # rotate
        right.appendleft(left.popleft())
        left.append(right.pop())

        print(left, right)

    return left[0]

print(solve_parttwo())