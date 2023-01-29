from itertools import cycle
from collections import Counter

spellbook = {
    # name : mana cost, damage, heal, armour, mana refund, effect
    # 'none' : [0, 0, 0, 0, 0, 0],
    'magic missile' : [53, 4, 0, 0, 0, 0],
    'drain' : [73, 2, 2, 0, 0, 0],
    'shield' : [113, 0, 0, 7, 0, 6],
    'poison' : [173, 3, 0, 0, 0, 6],
    'recharge' : [229, 0, 0, 0, 101, 5]
}


def choose_spell():
    for spell in cycle(spellbook.keys()):
        yield spell


def fight_spell_combat(hhp, hmana, ehp, eatt, active=Counter(), cast=[]):
    if hhp < 0:
        # print("You died (HP)")
        return False, cast

    if ehp < 0:
        # print("They died")
        return True, cast

    for spell in choose_spell():
        # print('considering', spell)

        if spellbook[spell][0] > hmana:
            # print("You died (Mana)")
            return False, cast

        elif active[spell] > 0:
            # print("Skipping already active", spell)
            continue

        elif spellbook[spell][5] == 0:
            # print("Instant", spell)

            hero_attack = spellbook[spell][1]
            hero_heal = spellbook[spell][2]
            hero_armour = 0
            hero_mana = 0

            for running in active:
                # print("Already active", running)
                if active[running] > 0:
                    active[running] -= 1
                    hero_attack += spellbook[running][1]
                    hero_heal += spellbook[running][2]
                    hero_armour += spellbook[running][3]
                    hero_mana += spellbook[running][4]

            yield from fight_spell_combat(hhp - max(eatt - hero_armour, 1) + hero_heal,
                                            hmana - spellbook[spell][0] + hero_mana,
                                            ehp - hero_attack,
                                            eatt,
                                            active,
                                            cast + [spell])

        else:
            # print("Adding to active", spell)

            hero_attack = 0
            hero_heal = 0
            hero_armour = 0
            hero_mana = 0

            for running in active:
                # print("Already active", running)
                if active[running] > 0:
                    active[running] -= 1
                    hero_attack += spellbook[running][1]
                    hero_heal += spellbook[running][2]
                    hero_armour += spellbook[running][3]
                    hero_mana += spellbook[running][4]

            active[spell] = spellbook[spell][5]

            yield from fight_spell_combat(hhp - max(eatt - hero_armour, 1) + hero_heal,
                                          hmana - spellbook[spell][0] + hero_mana,
                                          ehp - hero_attack,
                                          eatt,
                                          active,
                                          cast + [spell])


##
# here we go...

hit_points = 100 # 10 for test, 100 for live
mana_points = 500

with open('input.txt') as enemy_file:
    values = enemy_file.readlines()

enemy_hit_points = int(values[0].split(':')[1])
enemy_damage = int(values[1].split(':')[1])
# enemy_armour = int(values[2].split(':')[1])

wins = []
losses = []

hero_hp = hit_points
hero_mana = mana_points
enemy_hp = enemy_hit_points

winning_spells = []
for won, spells_cast in fight_spell_combat(hero_hp, hero_mana, enemy_hp, enemy_damage):
    if won:
        # print(f'{attack}, {armour} You died ({hero_hp} vs {enemy_hp})')
        print("Now to cost up the spells:", spells_cast)
        winning_spells.append(spells_cast)
