test = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''

syntax = []

import io
# with io.StringIO(test) as inputs:
with open('input10.txt') as inputs:
    for line in inputs:
        syntax.append(line.strip())

# print(syntax)
OPEN = ('(','[','{','<')
CLOSE = (')',']','}','>')
SYNTAX_SCORES = {')':3,']':57,'}':1197,'>':25137}
COMPLETION_SCORES = {')':1,']':2,'}':3,'>':4}

syntax_score = 0
for line in syntax:
    syntax_stack = []
    for ch in line:
        if ch in OPEN:
            syntax_stack.append(ch)
        else:
            opening = syntax_stack.pop()
            if OPEN.index(opening) != CLOSE.index(ch):
                # print('invalid:', ch, SCORES[ch])
                syntax_score += SYNTAX_SCORES[ch]
                break

print('syntax:', syntax_score)

closing_totals = []
for line in syntax:
    syntax_stack = []
    invalid = False
    for ch in line:
        if ch in OPEN:
            syntax_stack.append(ch)
        else:
            opening = syntax_stack.pop()
            if OPEN.index(opening) != CLOSE.index(ch):
                invalid = True
                break
    
    if not invalid and len(syntax_stack) > 0:
        closing = 0
        # print(syntax_stack)
        while len(syntax_stack) > 0:
            ch = syntax_stack.pop()
            closing *= 5
            closing += COMPLETION_SCORES[CLOSE[OPEN.index(ch)]]

        closing_totals.append(closing)

print('completion:', sorted(closing_totals)[len(closing_totals)//2])