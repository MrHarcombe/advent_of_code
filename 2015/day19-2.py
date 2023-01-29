test = '''e => H
e => O
H => HO
H => OH
O => HH

HOH'''

chemicals = []

import io
#with io.StringIO(test) as inputs:
with open('input.txt') as inputs:
    for line in inputs:
        if len(line.strip()) > 0:
            chemicals.append([s.strip() for s in line.split('=>')])
        else:
            break

    target = inputs.readline().strip()

import re

# current = target
# candidates = [(target, 0)]
# found = False
# for candidate, steps in candidates:
#     # print('candidate:', candidate)
#     if not found:
#         for chemical in chemicals:
#             if not found:
#                 c_in, c_out = chemical
#                 matches = re.finditer(c_out, target)
#                 for match in matches:
#                     # print(match.group(0), match.start())
#                     new = candidate[:match.start()] + c_in + candidate[match.end():]
#                     # print('new:', new)
#                     if new == 'e':
#                         print('done in:', steps+1)
#                         found = True
#                         break
#                     if (new, steps+1) not in candidates:
#                         candidates.append((new, steps+1))
#                         # print(candidates)

medicine = target
steps = 0
while medicine != 'e':
    for c_in, c_out in chemicals:
        if c_out in medicine:
            medicine = medicine.replace(c_out, c_in, 1)
            steps += 1

print(steps)
