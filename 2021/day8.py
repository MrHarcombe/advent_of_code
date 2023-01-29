test = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'''

def solve_line(numbers, inputs):
    cf = [number for number in numbers if len(number) == 2][0] # one
    acf = [number for number in numbers if len(number) == 3][0] # seven
    bcdf = [number for number in numbers if len(number) == 4][0] # four
    abcdefg = [number for number in numbers if len(number) == 7][0] # eight
    a = [ch for ch in acf if ch not in cf][0]

    two_three_five = [number for number in numbers if len(number) == 5]
    acdfg = '' # three
    # print('235:', two_three_five)
    adg = ''
    be = ''
    for digit in two_three_five:
        remaining = "".join([ch for ch in digit if ch not in cf])
        # print('remaining:', remaining)
        if len(remaining) == 3:
            acdfg = digit
            adg = remaining
        else:
            be += remaining
    be = ''.join([ch for ch in be if ch not in adg])

    # b = bcdf - adg - cf
    b = [ch for ch in bcdf if ch not in adg and ch not in cf][0]
    d = [ch for ch in bcdf if ch not in acf and ch != b][0]
    g = ''

    zero_six_nine = [number for number in numbers if len(number) == 6]
    # print('069:', zero_six_nine)
    for digit in zero_six_nine:
        remaining = "".join([ch for ch in digit if ch not in (a,b,d) and ch not in cf])
        if len(remaining) == 1:
            g = remaining[0]

    e = ''
    f = ''

    for digit in [digit for digit in two_three_five if digit != acdfg]:
        remaining = [ch for ch in digit if ch not in (a,b,d,g)]
        if len(remaining) == 1:
            f = remaining[0]
        else:
            e = [ch for ch in remaining if ch not in cf][0]

    c = [ch for ch in cf if ch != f][0]

    # print('a:', a, ' b:', b, ', c:', c, ', d:', d, ', e:', e, ', f:', f, ', g:', g)

    values = {
        "".join(sorted([a,b,c,e,f,g])) : '0',
        "".join(sorted([c,f])) : '1',
        "".join(sorted([a,c,d,e,g])) : '2',
        "".join(sorted([a,c,d,f,g])) : '3',
        "".join(sorted([b,c,d,f])) : '4',
        "".join(sorted([a,b,d,f,g])) : '5',
        "".join(sorted([a,b,d,e,f,g])) : '6',
        "".join(sorted([a,c,f])) : '7',
        "".join(sorted([a,b,c,d,e,f,g])) : '8',
        "".join(sorted([a,b,c,d,f,g])) : '9'
    }
    # print(values)

    string = ''
    for number in inputs:
        sorted_number = "".join(sorted(list(number)))
        string += values[sorted_number]

    return int(string)

import io
#with io.StringIO(test) as inputs:
with open('input8.txt') as inputs:
    count = 0
    total = 0
    for line in inputs:
        prefix, suffix = line.split(' | ')
        practice = prefix.strip().split()
        numbers = suffix.strip().split()
        # print(numbers)
        count += len([number for number in numbers if len(number) in (2,3,4,7)])
        total += solve_line(practice, numbers)

print('count:', count)
print('total:', total)
