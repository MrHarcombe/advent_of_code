from io import StringIO

test = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab"""

twos = 0
threes = 0

# with StringIO(test) as data:
with open("input2.txt") as data:
  for line in data:
    found_two = found_three = False
    
    for ch in set(line.strip()):
      if line.count(ch) == 2:
        found_two = True
      if line.count(ch) == 3:
        found_three = True

    if found_two: twos += 1
    if found_three: threes += 1

print("Part 1:", twos * threes)
