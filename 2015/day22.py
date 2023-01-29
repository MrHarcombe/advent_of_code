from io import StringIO

"""
Magic Missile costs 53 mana. It instantly does 4 damage.
Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
"""

## states
#
TURN = 0
PLAYER_HP = 1
CURRENT_MANA = 2
MANA_SPENT = 3
ARMOUR = 4
BOSS_HP = 5
BOSS_DAMAGE = 6
CAST_MM = 7
CAST_DRAIN = 8
CAST_SHIELD = 9
CAST_POISON = 10
CAST_RECHARGE = 11
LEFT_SHIELD = 12
LEFT_POISON = 13
LEFT_RECHARGE = 14

def apply_spell_effects(state, actions):
    turn_state = list(state)

    # move the turn count on
    turn_state[TURN] += 1
    actions.append(f"Turn: {turn_state[TURN]}")

    # part 2
    # on player turns, reduce player HP by 1
    if turn_state[TURN] % 2 == 1:
        turn_state[PLAYER_HP] -= 1

    # reset player armour (it will get set back up if applicable)
    turn_state[ARMOUR] = 0

    # apply existing effects
    if turn_state[LEFT_SHIELD] > 0:
        actions.append("shield in effect")
        turn_state[ARMOUR] = 7
        turn_state[LEFT_SHIELD] -= 1
        if turn_state[LEFT_SHIELD] == 0:
            actions.append("end of shield")
    if turn_state[LEFT_POISON] > 0:
        actions.append("poison in effect")
        turn_state[BOSS_HP] -= 3
        turn_state[LEFT_POISON] -= 1
        if turn_state[LEFT_POISON] == 0:
            actions.append("end of poison")
    if turn_state[LEFT_RECHARGE] > 0:
        actions.append("recharge in effect")
        turn_state[CURRENT_MANA] += 101
        turn_state[LEFT_RECHARGE] -= 1
        if turn_state[LEFT_RECHARGE] == 0:
            actions.append("end of recharge")

    return turn_state

def process_turns(player_turn, state):
    actions = []
    
    if player_turn:
        # player_turn_state = apply_spell_effects(state, actions)
        player_turn_state = list(state)

        # apply instant effects
        if player_turn_state[CAST_MM] == 1:
            actions.append("cast magic missile")
            player_turn_state[BOSS_HP] -= 4
            player_turn_state[CAST_MM] = 0
        if player_turn_state[CAST_DRAIN] == 1:
            actions.append("cast drain")
            player_turn_state[PLAYER_HP] += 2
            player_turn_state[BOSS_HP] -= 2
            player_turn_state[CAST_DRAIN] = 0

        # set new effect durations
        if player_turn_state[CAST_SHIELD] == 1:
            actions.append("cast shield")
            player_turn_state[LEFT_SHIELD] = 6
            player_turn_state[CAST_SHIELD] = 0
        if player_turn_state[CAST_POISON] == 1:
            actions.append("cast poison")
            player_turn_state[LEFT_POISON] = 6
            player_turn_state[CAST_POISON] = 0
        if player_turn_state[CAST_RECHARGE] == 1:
            actions.append("cast recharge")
            player_turn_state[LEFT_RECHARGE] = 5
            player_turn_state[CAST_RECHARGE] = 0

        return tuple(player_turn_state), actions

    else:
        boss_turn_state = apply_spell_effects(state, actions)

        if boss_turn_state[BOSS_HP] > 0:
            actions.append(f"boss hits for {boss_turn_state[BOSS_DAMAGE] - boss_turn_state[ARMOUR]}")
            boss_turn_state[PLAYER_HP] -= boss_turn_state[BOSS_DAMAGE] - boss_turn_state[ARMOUR]
        else:
            actions.append("boss died")

        return tuple(boss_turn_state), actions

def get_player_moves(state):
    possibles = []
    # turn_state, actions = process_turn(state)

    if state[CURRENT_MANA] >= 53:
        new_state = list(state)
        new_state[CURRENT_MANA] -= 53
        new_state[MANA_SPENT] += 53
        new_state[CAST_MM] = 1
        possibles.append(new_state)

    if state[CURRENT_MANA] >= 73:
        new_state = list(state)
        new_state[CURRENT_MANA] -= 73
        new_state[MANA_SPENT] += 73
        new_state[CAST_DRAIN] = 1
        possibles.append(new_state)

    if state[CURRENT_MANA] >= 113 and state[LEFT_SHIELD] == 0:
        new_state = list(state)
        new_state[CURRENT_MANA] -= 113
        new_state[MANA_SPENT] += 113
        new_state[CAST_SHIELD] = 1
        possibles.append(new_state)

    if state[CURRENT_MANA] >= 173 and state[LEFT_POISON] == 0:
        new_state = list(state)
        new_state[CURRENT_MANA] -= 173
        new_state[MANA_SPENT] += 173
        new_state[CAST_POISON] = 1
        possibles.append(new_state)

    if state[CURRENT_MANA] >= 229 and state[LEFT_RECHARGE] == 0:
        new_state = list(state)
        new_state[CURRENT_MANA] -= 229
        new_state[MANA_SPENT] += 229
        new_state[CAST_RECHARGE] = 1
        possibles.append(new_state)

    return possibles

def depth_first(initial):
    stack = [(initial, [])]
    visited = set()

    while len(stack) > 0:
        current_state, current_actions = stack.pop()
        visited.add((current_state, tuple(current_actions)))

        if current_state[BOSS_HP] <= 0:
            yield current_state, current_actions

        else:
            turn_actions = []
            player_state = apply_spell_effects(current_state, turn_actions)
            next_states = get_player_moves(player_state)
            for next_state in next_states:
                # process player action and boss action
                boss_state, player_actions = process_turns(True, next_state)
                outcome, boss_actions = process_turns(False, boss_state)
                actions = list(current_actions) + turn_actions + player_actions + boss_actions
                if outcome[PLAYER_HP] > 0 and (tuple(outcome), tuple(actions)) not in visited:
                    stack.append((tuple(outcome), actions))

    yield (0, 0, 0, float("inf"), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), ["Nothing found"]

test = """Hit points: 14
Damage: 8"""

## My test
# Player 9, 750
# Boss 24, 8

## Standard test
# Player 10, 250

player_hp = 50
player_mana = 500

# with StringIO(test) as f:
with open("input22.txt") as f:
    boss_hp, boss_damage = [int(n.split(":")[1]) for n in f.readlines()]

initial_state = (0, player_hp, player_mana, 0, 0, boss_hp, boss_damage, 0, 0, 0, 0, 0, 0, 0, 0)

print("Player HP:", player_hp)
print("Player mana:", player_mana)
print("Boss HP:", boss_hp)
print("Boss damage:", boss_damage)

state, actions = min(depth_first(initial_state), key=lambda i:i[0][MANA_SPENT])
for action in actions:
    print(action)
print(state)
# lowest_cost = float("inf")
# for state, actions in depth_first(initial_state):
#     if state[13] < lowest_cost:
#         lowest_cost = state[13]
#         print(state, actions)
