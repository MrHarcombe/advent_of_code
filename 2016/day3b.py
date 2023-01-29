from itertools import permutations

lines = []

with open("input3.txt") as f:
    for line in f:
        values = [int(n) for n in line.split()]
        lines.append(values)
    
triangles = []
for i in range(0, len(lines), 3):
    for j in range(3):
        triangles.append([lines[i][j], lines[i+1][j], lines[i+2][j]])
        
possibles = 0
for t in triangles:
    #print(t)
    possible = True
    for s1,s2,s3 in permutations(t):
        if s1+s2<=s3:
            possible = False
    if possible:
        possibles += 1
        
print(possibles)
