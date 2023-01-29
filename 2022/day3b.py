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
        contents1 = set(line.strip())
        contents2 = set(f.readline().strip())
        contents3 = set(f.readline().strip())

        #print(contents1.intersection(contents2,contents3))
        priorities.append(*contents1.intersection(contents2,contents3))

print(sum([1+ord(ch) - ((ord("A") - 26) if ch.isupper() else ord("a")) for ch in priorities]))
