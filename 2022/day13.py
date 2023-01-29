from io import StringIO
import json

test = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

def compare_part(left, right):
    if isinstance(left, int) and isinstance(right, int):
        # print("Comparing ints", left, right)
        if left < right:
            return True
        elif left > right:
            return False

    elif isinstance(left, list) and isinstance(right, list):
        # print("Comparing lists", left, right)
        pos = 0
        while pos < len(left) and pos < len(right):
            result = compare_part(left[pos], right[pos])
            if result != None:
                return result
            pos += 1
        
        if pos == len(left) and pos < len(right):
            return True
        elif pos < len(left):
            return False

    elif isinstance(left, int):
        # print("Comparing int with list", left, right)
        return compare_part([left], right)
        
    elif isinstance(right, int):
        # print("Comparing list with int", left, right)
        return compare_part(left, [right])

    return None

# with StringIO(test) as f:
with open("input13.txt") as f:
    index = 0
    total = 0
    for line in f:
        index += 1
        left = json.loads(line)
        right = json.loads(f.readline())
        f.readline()

        if compare_part(left, right):
            total += index

    print(total)