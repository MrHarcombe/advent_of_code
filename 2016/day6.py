from collections import Counter
import io

test = '''eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar'''

letters = [Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter()]

# with io.StringIO(test) as file:
with open('input6.txt') as file:
    for line in file:
        for i, ch in enumerate(line.strip()):
            letters[i][ch] += 1
            
print([sorted(n.items(), key=lambda pair: pair[1])[0] for n in letters])


