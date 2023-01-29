from collections import defaultdict, Counter

dice_combinations = Counter()

for i in range(1,4):
    for j in range(1,4):
        for k in range(1,4):
            dice_combinations[i+j+k] += 1

positions = []
# positions.append((4,8))
positions.append((7,3))

scores = []
scores.append((0,0))

universes = []
universes.append(1)

wins = Counter()
turn = 0

while len(positions) > 0:
    new_positions = []
    new_scores = []
    new_universes = []

    player = turn % 2

    for i, (p1, p2) in enumerate(positions):
        s1, s2 = scores[i]
        u = universes[i]

        for roll, count in dice_combinations.items():
            if player == 0: # player1
                new_p1 = (((p1 - 1) + roll) % 10) + 1
                new_score = s1 + new_p1

                if new_score >= 21:
                    wins[1] += count * u

                else:
                    new_positions.append((new_p1, p2))
                    new_scores.append((new_score, s2))
                    new_universes.append(u * count)
            else:
                new_p2 = (((p2 - 1) + roll) % 10) + 1
                new_score = s2 + new_p2

                if new_score >= 21:
                    wins[2] += count * u

                else:
                    new_positions.append((p1, new_p2))
                    new_scores.append((s1, new_score))
                    new_universes.append(u * count)

    turn += 1
    positions = new_positions
    scores = new_scores
    universes = new_universes

# print('pos:', positions)
# print('scores:', scores)
# print('uni:', universes)     
print(wins)