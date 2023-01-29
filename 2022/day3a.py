from io import StringIO

test = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

priorities = []
#with StringIO(test) as f:
with open("input3.txt") as f:
    for line in f:
        contents = line.strip()
        left, right = set(contents[:len(contents)//2]), set(contents[len(contents)//2:])
        #print(left.intersection(right))
        priorities.append(*left.intersection(right))

print(sum([1+ord(ch) - ((ord("A") - 26) if ch.isupper() else ord("a")) for ch in priorities]))
