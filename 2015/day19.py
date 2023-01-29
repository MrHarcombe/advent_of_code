test = '''H => HO
H => OH
O => HH

HOHOHO'''

chemicals = []
final = set()

import io
#with io.StringIO(test) as inputs:
with open('input.txt') as inputs:
    for line in inputs:
        if len(line.strip()) > 0:
            chemicals.append([s.strip() for s in line.split('=>')])
        else:
            break

    starting_point = inputs.readline().strip()

import re

print(chemicals, starting_point)
for chemical in chemicals:
    c_in, c_out = chemical
    matches = re.finditer(c_in, starting_point)
    for match in matches:
        #print(match.group(0), match.start())
        final.add(starting_point[:match.start()] + c_out + starting_point[match.end():])

print(len(final))