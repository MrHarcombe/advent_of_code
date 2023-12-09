from io import StringIO

test = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

report = []

def get_next_value(seq):
    # is it arithmetic?
    # if seq[1] - seq[0] == seq[-1] - seq[-2]:
    #     return seq[-1] + (seq[0] - seq[-1])
    
    # okay, so let's get geometric?? aargh!!
    
    all_diffs = []
    all_same = False
    this_seq = seq
    while not all_same:
        diffs = [this_seq[i+1] - this_seq[i] for i in range(len(this_seq)-1)]
        all_same = len(set(diffs)) == 1
        all_diffs.append(diffs)
        this_seq = diffs

    d = all_diffs.pop()
    value = d.pop()
    while len(all_diffs) > 0:
        d = all_diffs.pop()
        value += d.pop()

    return seq[-1] + value

def get_previous_value(seq):
    all_diffs = []
    all_same = False
    this_seq = seq
    while not all_same:
        diffs = [this_seq[i+1] - this_seq[i] for i in range(len(this_seq)-1)]
        all_same = len(set(diffs)) == 1
        all_diffs.append(diffs)
        this_seq = diffs

    d = all_diffs.pop()
    value = d.pop(0)
    # print(value, d)
    while len(all_diffs) > 0:
        d = all_diffs.pop()
        dvalue = d.pop(0)
        # print(dvalue, d)
        value = dvalue - value

    # print("<--", seq[0] - value)
    return seq[0] - value

# with StringIO(test) as data:
with open("input9.txt") as data:
    for line in data:
        report.append(list(map(int, line.strip().split())))

print("Part 1:", sum([get_next_value(line) for line in report]))
print("Part 2:", sum([get_previous_value(line) for line in report]))