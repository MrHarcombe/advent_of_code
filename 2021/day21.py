from itertools import product
import io

test = '''Player 1 starting position: 4
Player 2 starting position: 8'''


class quantum_die():
    def __init__(self, highest):
        self.highest = highest


    def rolls(self):
        return product(range(1, self.highest+1), repeat=self.highest)


class deterministic_die():
    def __init__(self, highest):
        self.highest = highest
        self.current = 0
        self.rolls = 0

    
    def roll(self):
        self.rolls += 1
        self.current = self.current % self.highest
        self.current += 1
        return self.current


p1_pos, p1_score = 0, 0
p2_pos, p2_score = 0, 0

with io.StringIO(test) as inputs:
# with open('input21.txt') as inputs:
    p1_pos = int(inputs.readline().split(":")[1])
    p2_pos = int(inputs.readline().split(":")[1])

print(p1_pos, p2_pos)

WINNING_SCORE = 21


def part_one(p1_pos, p2_pos, p1_score, p2_score):
    die = deterministic_die(100)

    while p1_score < WINNING_SCORE and p2_score < WINNING_SCORE:
        p1_r1, p1_r2, p1_r3 = die.rolls()
        print(p1_r1, p1_r2, p1_r3)
        p2_r1, p2_r2, p2_r3 = die.rolls()
        print(p2_r1, p2_r2, p2_r3)

        p1_pos = (((p1_pos - 1) + sum((p1_r1, p1_r2, p1_r3))) % 10) + 1
        p1_score += p1_pos
        # print("P1", p1_pos, p1_score)

        if p1_score < WINNING_SCORE:
            p2_pos = (((p2_pos - 1) + sum((p2_r1, p2_r2, p2_r3))) % 10) + 1
            p2_score += p2_pos
            # print("P2", p2_pos, p2_score)

# print(p1_score, p2_score, die.rolls)
# print(die.rolls * (p1_score if p1_score < 1000 else p2_score))


def part2_turn(p1_pos, p2_pos, p1_score, p2_score):
    # print(f'Here we go again {p1_pos}/{p1_score}, {p2_pos}/{p2_score}...')
    # p1_die = quantum_die(3)
    # p2_die = quantum_die(3)

    p1_wins = 0
    p2_wins = 0

    for p1_r1, p1_r2, p1_r3 in product((1,2,3), repeat=3):
        new_p1_pos = (((p1_pos - 1) + sum((p1_r1, p1_r2, p1_r3))) % 10) + 1
        new_p1_score = p1_score + new_p1_pos

        if new_p1_score >= WINNING_SCORE:
            p1_wins += 1

        else:
            for p2_r1, p2_r2, p2_r3 in product((1,2,3), repeat=3):

                new_p2_pos = (((p2_pos - 1) + sum((p2_r1, p2_r2, p2_r3))) % 10) + 1
                new_p2_score = p2_score + new_p2_pos

                if new_p2_score >= WINNING_SCORE:
                    p2_wins += 1

                else:
                    p1_subwins, p2_subwins = part2_turn(new_p1_pos, new_p2_pos, new_p1_score, new_p2_score)
                    p1_wins += p1_subwins
                    p2_wins += p2_subwins

    # print(p1_wins, p2_wins)
    return p1_wins, p2_wins


print(part2_turn(p1_pos, p2_pos, 0, 0))
