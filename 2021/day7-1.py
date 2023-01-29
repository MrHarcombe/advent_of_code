test = '''16,1,2,0,4,2,7,1,2,14'''

import io
#with io.StringIO(test) as inputs:
with open('input7.txt') as inputs:
    crabs = [int(n) for n in inputs.readline().split(',')]

left = min(crabs)
right = max(crabs)

def triangular(n):
    # return sum([t for t in range(1,n+1)])
    return ((1 + n) * n) // 2

#print(left, right, crabs)
best_cost = float('inf')
for meet in range(left, right+1):
    cost = sum([triangular(abs(meet - n)) for n in crabs])
    if cost < best_cost:
        best_cost = cost

print(best_cost)
