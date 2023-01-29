from io import StringIO

""" possible moves...

    R R
    R P
    R S
    P R
    P P
    P S
    S R
    S P
    S S
    
"""

def score1(p1, p2):
    score = p2
    if p1 == 1:
        if p2 == 1:
            score += 3
        elif p2 == 2:
            score += 6
            
    elif p1 == 2:
        if p2 == 2:
            score += 3
        elif p2 == 3:
            score += 6
            
    elif p1 == 3:
        if p2 == 1:
            score += 6
        elif p2 == 3:
            score += 3

    return score

def score2(p1, outcome):
    score = 0
    
    if outcome == 2:
        score = 3 + p1
    
    elif p1 == 1:
        if outcome == 1:
            score = 0 + 3
        else:
            score = 6 + 2
            
    elif p1 == 2:
        if outcome == 1:
            score = 0 + 1
        else:
            score = 6 + 3
            
    elif p1 == 3:
        if outcome == 1:
            score = 0 + 2
        else:
            score = 6 + 1

    return score

test = """A Y
B X
C Z"""

rps = str.maketrans("ABCXYZ", "123123")

total1 = 0
total2 = 0
#with StringIO(test) as f:
with open("input2.txt") as f:
    for line in f:
        inputs = [int(n) for n in line.translate(rps).split()]
        total1 += score1(*inputs)
        total2 += score2(*inputs)
print(total1, total2)
        