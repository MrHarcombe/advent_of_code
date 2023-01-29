from io import StringIO
from itertools import permutations

def swap_positions(phrase, x, y):
    """swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped."""
    low, high = min(x,y), max(x,y)
    return phrase[:low] + phrase[high] + phrase[low+1:high] + phrase[low] + phrase[high+1:]
    
def swap_letters(phrase, x, y):
    """"swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the string)."""
    xpos, ypos = phrase.index(x), phrase.index(y)
    low, high = min(xpos,ypos), max(xpos,ypos)
    return phrase[:low] + phrase[high] + phrase[low+1:high] + phrase[low] + phrase[high+1:]

def rotate_steps(phrase, x, right=True):
    """rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc."""
    x = x % len(phrase)
    if right:
        return phrase[-x:] + phrase[:-x]
    return phrase[x:] + phrase[:x]

def rotate_on_position(phrase, x):
    """rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4."""
    xpos = phrase.index(x) + 1
    if xpos > 4:
        xpos += 1
    return rotate_steps(phrase, xpos)    

def reverse_letters(phrase, x, y):
    """reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order."""
    span = phrase[x:y+1][::-1]
    return phrase[:x] + span + phrase[y+1:]

def move_position(phrase, x, y):
    """move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y."""
    moving = phrase[x]
    interim = phrase[:x] + phrase[x+1:]
    return interim[:y] + moving + interim[y:]

test = """swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d"""

# seed = "abcde"
start = "abcdefgh"
target = "fbgdceah"

for possible in permutations(start):
    seed = "".join(possible)
    
    # with StringIO(test) as f:
    with open("input21.txt") as f:
        for line in f:
            parts = line.strip().split()
            if parts[0] == "reverse":
                seed = reverse_letters(seed, int(parts[2]), int(parts[4]))
            elif parts[0] == "move":
                seed = move_position(seed, int(parts[2]), int(parts[5]))
            elif parts[0] == "swap":
                if parts[1] == "position":
                    seed = swap_positions(seed, int(parts[2]), int(parts[5]))
                else:
                    seed = swap_letters(seed, parts[2], parts[5])
            elif parts[0] == "rotate":
                if parts[1] == "left":
                    seed = rotate_steps(seed, int(parts[2]), False)
                elif parts[1] == "right":
                    seed = rotate_steps(seed, int(parts[2]))
                else:
                    seed = rotate_on_position(seed, parts[6])
                    
            # print(seed)

    if seed == target:
        print("".join(possible), "->", target)
        break
