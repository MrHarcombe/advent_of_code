data = {}

with open('input.txt') as input_data:
    for line in input_data:
        colon = line.index(':')
        sue = line[0:colon]
        details = line[colon+1:].strip().split(',')
        for key in details:
            word, value = [s.strip() for s in key.strip().split(':')]
            if word in data:
                dataset = data[word]
            else:
                dataset = {}
                data[word] = dataset
            
            value = int(value)
            if value in dataset:
                dataset[value].append(sue)
            else:
                dataset[value] = [sue]

# print(data)

ticker = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1'''

sues = {}

import io
with io.StringIO(ticker) as details:
    for detail in details:
        fact, value = [s.strip() for s in detail.split(':')]
        value = int(value)
        if fact in ['cats', 'trees']:
            for i in range(value+1, max(data[fact])+1):
                candidates = data[fact][i]
                for sue in candidates:
                    if sue in sues:
                        sues[sue] += 1
                    else:
                        sues[sue] = 1
        elif fact in ['pomeranians', 'goldfish']:
            for i in range(value-1, -1, -1):
                candidates = data[fact][i]
                for sue in candidates:
                    if sue in sues:
                        sues[sue] += 1
                    else:
                        sues[sue] = 1
        else:
            candidates = data[fact][value]
            for sue in candidates:
                if sue in sues:
                    sues[sue] += 1
                else:
                    sues[sue] = 1

most = max(sues.values())
for k,v in sues.items():
    if v == most:
        print(k)
