import re
from collections import Counter

DIRAC_ROLLS = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def dirac_play(p1_start, p2_start):
    game_states = Counter()
    game_states[((p1_start - 1, 0), (p2_start - 1, 0))] = 1
    wins = [0, 0]
    rnd_cnt = 0

    while game_states:
        new_states = Counter()
        p = rnd_cnt % 2

        for state, n_universe in game_states.items():
            for roll, n_rolls in DIRAC_ROLLS.items():
                new_s = list(state)
                new_pos = (state[p][0] + roll) % 10
                new_score = state[p][1] + new_pos + 1

                if new_score >= 21:
                    wins[p] += n_universe * n_rolls
                else:
                    new_s[p] = (new_pos, new_score)
                    new_states[tuple(new_s)] += n_universe * n_rolls

        rnd_cnt += 1
        game_states = new_states

    return wins


def play(player_1_start, player_2_start):
    score = [0, 0]
    pos = [player_1_start - 1, player_2_start - 1]
    rnd_cnt = 0
    while max(score) < 1000:
        p = rnd_cnt % 2
        roll = (9 * rnd_cnt + 6) % 100
        pos[p] = (pos[p] + roll) % 10
        score[p] += pos[p] + 1
        rnd_cnt += 1

    return (score, rnd_cnt)


def parse_data(puzzle_input):
    return [
        int(n)
        for n in re.search(
            r"Player 1 starting position: (\d+)\nPlayer 2 starting position: (\d+)",
            puzzle_input,
        ).groups()
    ]


def solution_1(puzzle_input):
    start_pos = parse_data(puzzle_input)
    score, rnd_cnt = play(*start_pos)
    return min(score) * (rnd_cnt) * 3


def solution_2(puzzle_input):
    start_pos = parse_data(puzzle_input)
    return max(dirac_play(*start_pos))

print(solution_2('''Player 1 starting position: 4
Player 2 starting position: 8'''))