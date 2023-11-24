import sys
sys.path.append('..')

from io import StringIO
from structures import RedBlackTree

test = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"""

warehouse = RedBlackTree()
# with StringIO(test) as data:
with open("input2.txt") as data:
  for line in data:
    warehouse.add(line.strip())

prev = None
def compare_previous(node):
  global prev
  if prev != None:
    # print("Comparing", prev.value, node.value)
    if len(prev.value) == len(node.value):
      diffs = []
      for i, ch in enumerate(prev.value):
        if ch != node.value[i]:
          diffs.append(i)

      if len(diffs) == 1:
        print(node.value[:diffs[0]]+node.value[diffs[0]+1:])

  # now this is the new previous
  prev = node

warehouse.in_traverse(compare_previous)