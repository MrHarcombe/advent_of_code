from io import StringIO

test = """16
10
15
5
1
11
7
19
6
12
4"""

test = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

# with StringIO(test) as data:
with open("input10.txt") as data:
    adaptors = sorted(list(map(int, data.readlines())))
    
previous = 0
diffs = []
for i in range(len(adaptors)):
    diffs.append(adaptors[i] - previous)
    previous = adaptors[i]

print("Part 1:", diffs.count(1) * (diffs.count(3) + 1))

def count_ways(pos, adaptors, store):
 
    if (pos <= 0):
        return 1
 
    if(store[pos] != -1):
        return store[pos]
 
    store[pos] = 0

    # check for 1, 2, 3 less
    possibles = [n for n in range(1,4) if pos-n in range(len(adaptors)) and adaptors[pos] - adaptors[pos-n] in range(1,4)]
    for n in possibles:
        store[pos] += count_ways(pos-n, adaptors, store)

    return store[pos]

##
# don't forget the wall socket is 0 and the final built-in adaptor always steps up by 3
adaptors.insert(0, 0)
adaptors.append(adaptors[-1]+3)

ways = [-1 for i in range(len(adaptors))]
print("Part 2:", count_ways(len(adaptors)-1, adaptors, ways))
