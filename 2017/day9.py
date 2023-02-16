from io import StringIO

test = """{{{},{},{{}}}}
{<a>,<a>,<a>,<a>}
{{<ab>},{<ab>},{<ab>},{<ab>}}
{{<!!>},{<!!>},{<!!>},{<!!>}}
{{<a!>},{<a!>},{<a!>},{<ab>}}"""

# with StringIO(test) as f:
with open("input9.txt") as f:
    stream = [l.strip() for l in f.readlines()]

def score_line(line):
    group_score = 0
    non_garbage_score = 0
    in_group = 0
    in_garbage = False
    cancel = False

    for ch in line:
        if in_garbage and not cancel and ch not in (">","!"):
            non_garbage_score += 1

        if ch == "{" and not in_garbage and not cancel:
            in_group += 1
        elif ch == "<" and not in_garbage and not cancel:
            in_garbage = True
        elif ch == ">" and in_garbage and not cancel:
            in_garbage = False
        elif ch == "}" and not in_garbage and not cancel:
            group_score += in_group
            in_group -= 1
        elif ch == "!" or cancel:
            cancel = not cancel

    return group_score, non_garbage_score

p1_score = 0
p2_score = 0
for line in stream:
    p1_score, p2_score = score_line(line)

print("Part 1:", p1_score)
print("Part 2:", p2_score)
