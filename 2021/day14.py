import io, re

test='''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''

start = ''
pairs = {}

# with io.StringIO(test) as inputs:
with open('input14.txt') as inputs:
    start = inputs.readline().strip()
    inputs.readline()
    for line in inputs:
        match, to = line.strip().split(' -> ')
        pairs[re.compile(match)] = to

print('start:', start, 'pairs:', pairs)

steps = 40
output = start

for i in range(steps):
    matches = []
    for j in range(len(output)):
        for search in pairs:
            match = search.match(output, j)
            if match:
                matches.append(match)
                break
        # for match in re.finditer(search, output):
        #     matches.append(match)

    matches = sorted(matches, key=lambda m: m.start())
    # print(len(matches), matches)
    offset = 0
    for match in matches:
        # print(match)
        output = output[:match.start()+offset+1] + pairs[match.re] + output[match.end()+offset-1:]
        offset += len(pairs[match.re])
        # print(output, offset)
    print(f'finished {i}, output is length {len(output)}')

# print(output)
elements = {}
for ch in list(output):
    if ch in elements:
        elements[ch] += 1
    else:
        elements[ch] = 1
el_counts = []
for el, count in elements.items():
    el_counts.append((el, count))
el_counts.sort(key=lambda e: e[1])
print(el_counts[0], el_counts[-1])
print(el_counts[-1][1] - el_counts[0][1])