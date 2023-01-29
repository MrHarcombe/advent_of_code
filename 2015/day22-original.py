from io import StringIO

"""
Magic Missile costs 53 mana. It instantly does 4 damage.
Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
"""

## state
#  0- player HP
#  1- player mana
#  2- player armour
#  3- boss HP
#  4- boss damage
#  5- use magic missile
#  6- use drain
#  7- use shield
#  8- use poison
#  9- use recharge
# 10- shield remaining
# 11- poison remaining
# 12- recharge remaining
# 13- mana spent

def process_turn(turn, state):
    if turn == 0: return state, []

    actions = []
    actions.append(f"turn: {turn}")
    turn_state = list(state)

    # reset player armour (it will get set back up if applicable)
    turn_state[2] = 0

    # apply existing effects
    if state[10] > 0:
        actions.append("shield in effect")
        turn_state[2] = 7
        turn_state[10] -= 1
    if state[11] > 0:
        actions.append("poison in effect")
        turn_state[3] -= 3
        turn_state[11] -= 1
    if state[12] > 0:
        actions.append("recharge in effect")
        turn_state[1] += 101
        turn_state[12] -= 1

    if turn % 2 == 1:
        # apply instant effects
        if state[5] == 1:
            actions.append("cast magic missile")
            turn_state[3] -= 4
            turn_state[5] = 0
        if state[6] == 1:
            actions.append("cast drain")
            turn_state[0] += 2
            turn_state[3] -= 2
            turn_state[6] = 0

        # set new effect durations
        if state[7] == 1:
            actions.append("cast shield")
            turn_state[10] = 6
            turn_state[7] = 0
        if state[8] == 1:
            actions.append("cast poison")
            turn_state[11] = 6
            turn_state[8] = 0
        if state[9] == 1:
            actions.append("cast recharge")
            turn_state[12] = 5
            turn_state[9] = 0

    elif turn_state[3] > 0:
        actions.append(f"boss hits for {turn_state[4] - turn_state[2]}")
        turn_state[0] -= turn_state[4] - turn_state[2]

    return tuple(turn_state), actions

def get_possible_states(turn, state):
    possibles = []
    # turn_state, actions = process_turn(turn, state)

    if turn % 2 == 1:
        return [state]

    if state[1] >= 53:
        new_state = list(state)
        new_state[1] -= 53
        new_state[13] += 53
        new_state[5] = 1
        possibles.append(new_state)

    if state[1] >= 73:
        new_state = list(state)
        new_state[1] -= 73
        new_state[13] += 73
        new_state[6] = 1
        possibles.append(new_state)

    if state[1] >= 113 and state[10] == 0:
        new_state = list(state)
        new_state[1] -= 113
        new_state[13] += 113
        new_state[7] = 1
        possibles.append(new_state)

    if state[1] >= 173 and state[11] == 0:
        new_state = list(state)
        new_state[1] -= 173
        new_state[13] += 173
        new_state[8] = 1
        possibles.append(new_state)

    if state[1] >= 229 and state[12] == 0:
        new_state = list(state)
        new_state[1] -= 229
        new_state[13] += 229
        new_state[9] = 1
        possibles.append(new_state)

    return possibles

def depth_first(initial):
    stack = [(0, initial, [])]
    visited = set()

    while len(stack) > 0:
        current_depth, current_state, current_actions = stack.pop()
        visited.add((current_depth, current_state))

        if current_state[3] <= 0:
            yield current_state, current_actions

        else:
            next_states = get_possible_states(current_depth, current_state)
            for next_state in next_states:
                outcome, actions = process_turn(current_depth + 1, next_state)
                if outcome[0] > 0 and (current_depth + 1, tuple(outcome)) not in visited:
                    stack.append((current_depth + 1, tuple(outcome), list(current_actions) + actions))

    yield (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, float("inf")), ["Nothing found"]

test = """Hit points: 15
Damage: 8"""

player_hp = 50 # 10
player_mana = 500 # 250

# with StringIO(test) as f:
with open("input22.txt") as f:
    boss_hp, boss_damage = [int(n.split(":")[1]) for n in f.readlines()]

initial_state = (player_hp, player_mana, 0, boss_hp, boss_damage, 0, 0, 0, 0, 0, 0, 0, 0, 0)

print("Player HP:", player_hp)
print("Player mana:", player_mana)
print("Boss HP:", boss_hp)
print("Boss damage:", boss_damage)

# print(min(depth_first(initial_state), key=lambda i:i[0][13]))
lowest_cost = float("inf")
for state, actions in depth_first(initial_state):
    if state[13] < lowest_cost:
        lowest_cost = state[13]
        print(state, actions)
