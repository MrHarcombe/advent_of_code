from itertools import permutations

possibles = 0
with open("input3.txt") as f:
    for line in f:
        parts = line.split()
        sides = [int(n) for n in parts]

        possible = True
        for s1, s2, s3 in permutations(sides):
            if s1 + s2 <= s3:
                possible = False
        
        if possible:
            possibles += 1
            
print(possibles)
