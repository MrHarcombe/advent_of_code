from io import StringIO
import re

CONTAINS_DIGIT = re.compile(r"[0-9]")

def expand_subrule(rule):
    rule_parts = rule.split()
    for i in range(len(rule_parts)):
        if rule_parts[i].isdigit():
            sub_rule = rule_parts[i]
            break

    prefix = " ".join(rule_parts[:i])
    suffix = " ".join(rule_parts[i+1:])

    if "|" in rules[sub_rule]:
        return prefix + " ( " + rules[sub_rule] + " ) " + suffix
    else:
        return prefix + " " + rules[sub_rule] + " " + suffix

test = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb'''

rules = {}
terminals = {}
possibles = []

# with StringIO(test) as data:
with open("input19.txt") as data:
    for line in data:
        if len(line.strip()) > 0:
            if ":" in line:
                rule, content = line.strip().split(":")
                if '"' in content:
                    terminals[rule] = content.replace('"', '')
                    rules[rule] = content.replace('"', '')
                else:
                    rules[rule] = content.strip()
            else:
                possibles.append(line.strip())

# for k in rules:
#     for t in terminals:
#         rules[k] = rules[k].replace(t, terminals[t])

rules["8"] = "42 +"
rules["11"] = "42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31 | 42 42 42 42 42 31 31 31 31 31"

expansion = ""
queue = [rules["0"]]
while len(queue) > 0:
    rule = queue.pop(0)
    alt = expand_subrule(rule)
    if CONTAINS_DIGIT.search(alt):
        queue.append(alt)
    else:
        expansion = re.compile("^" + alt.replace(" ", "") + "$")

print(expansion.pattern)

count = 0
for possible in possibles:
    if expansion.match(possible):
        # print("Matched:", possible, f"({len(possible)})")
        count += 1
        
print("Matched:", count)

# 329 too high
# 305 too high
