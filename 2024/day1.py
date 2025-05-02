from io import StringIO
from collections import Counter

test = """3   4
4   3
2   5
1   3
3   9
3   3"""

list1 = []
list2 = []

# with StringIO(test) as list_data:
with open("input1.txt") as list_data:
    for line in list_data:
        num1, num2 = map(int, line.strip().split())
        list1.append(num1)
        list2.append(num2)

# print(list1, list2)

total = 0
for p1, p2 in zip(sorted(list1), sorted(list2)):
    total += abs(p1 - p2)

print("Part 1:", total)

similarity = 0
c2 = Counter(list2)
for num in list1:
    if num in c2:
        similarity += num * c2[num]
print("Part 2:", similarity)