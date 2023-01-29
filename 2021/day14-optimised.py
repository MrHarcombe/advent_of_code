import io

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

working_pairs = {}
match_pairs = {}
letter_counts = {}

# with io.StringIO(test) as inputs:
with open('input14.txt') as inputs:
    start = inputs.readline().strip()
    for i in range(len(start) - 1):
        working_pairs[''.join(start[i:i+2])] = 1

    for ch in start:
        if ch in letter_counts:
            letter_counts[ch] += 1
        else:
            letter_counts[ch] = 1

    inputs.readline()
    for line in inputs:
        match, to = line.strip().split(' -> ')
        match_pairs[match] = to
        if match not in working_pairs:
            working_pairs[match] = 0

print(working_pairs)

steps = 40
for i in range(steps):
    for pair, count in list(working_pairs.items()):
        # print(pair, count)
        if count > 0:
            # print(f'{pair} currently at {count}')
            new_letter = match_pairs[pair]
            # print('new letter:', new_letter)
            if new_letter in letter_counts:
                letter_counts[new_letter] += count
            else:
                letter_counts[new_letter] = count

            scratch = pair[0]+new_letter
            # print('first scratch:', scratch)
            if scratch in working_pairs:
                working_pairs[scratch] += count
            else:
                working_pairs[scratch] = count
            
            scratch = new_letter+pair[1]
            # print('second scratch:', scratch)
            if scratch in working_pairs:
                working_pairs[scratch] += count
            else:
                working_pairs[scratch] = count

            working_pairs[pair] -= count

        # print('working_pairs:', working_pairs)

print(letter_counts)
print(max(letter_counts.values()) - min(letter_counts.values()))
