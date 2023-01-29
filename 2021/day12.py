from itertools import permutations
from functools import reduce
from operator import add

smallest = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''

larger = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc'''

largest = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''

paths = {'starts' : [], 'routes' : [], 'ends' : []}

def cannot_revisit(next_cave, visited):
    if part1:
        return next_cave in visited

    already_visited = {}
    for cave in [c for c in visited if c.islower()]:
        if cave in already_visited:
            already_visited[cave] += 1
        else:
            already_visited[cave] = 1

    return next_cave in already_visited and max(already_visited.values()) > 1

def generate_paths(paths, current=None, visited=[]):
    # print('current:', current, 'visited:', visited)

    # check for endings
    if current != None:
        for last,_ in paths['ends']:
            if current == last:
                yield visited

    if len(visited) == 0:
        for _,current in paths['starts']:
            if current.islower() and cannot_revisit(current, visited):
                continue
            yield from generate_paths(paths, current, visited+[current])

    else:
        # for fro,to in reduce(add, permutations(paths['routes'], len(paths['routes']))):
        # print(current,visited)
        for fro,to in paths['routes']:
            if current == fro:
                if to.islower() and cannot_revisit(to, visited):
                    continue
                yield from generate_paths(paths, to, visited+[to])
            elif current == to:
                if fro.islower() and cannot_revisit(fro, visited):
                    continue
                yield from generate_paths(paths, fro, visited+[fro])

import io
# with io.StringIO(smallest) as inputs:
with open('input12.txt') as inputs:
    for line in inputs:
        fro, to = line.strip().split('-')
        if fro == 'start':
            paths['starts'].append((fro,to))
        elif to == 'start':
            paths['starts'].append((to,fro))
        elif fro == 'end':
            paths['ends'].append((to,fro))
        elif to == 'end':
            paths['ends'].append((fro,to))
        else:
            paths['routes'].append((fro,to))

print(paths)
# print(list(permutations(paths['routes'], len(paths['routes']))))
# print(reduce(add, permutations(paths['routes'], len(paths['routes']))))
part1 = True
complete_paths = set()
for path in generate_paths(paths):
    complete_paths.add(''.join(path))
print('total paths:', len(complete_paths))

part1 = False
complete_paths = set()
for path in generate_paths(paths):
    complete_paths.add(''.join(path))
print('total paths:', len(complete_paths))
