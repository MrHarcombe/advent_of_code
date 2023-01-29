from collections import Counter

combinations = Counter()

for i in range(1,4):
    for j in range(1,4):
        for k in range(1,4):
            combinations[i+j+k] += 1

print(combinations)
