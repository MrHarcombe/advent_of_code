shop = '''Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3'''

shop = {
    'weapons' : {
        'dagger' : [8, 4, 0],
        'shortsword' : [10, 5, 0],
        'warhammer' : [25, 6, 0],
        'longsword' : [40, 7, 0],
        'greatsword' : [74, 8, 0]
    },
    'armour' : {
        'leather' : [13, 0, 1],
        'chainmail' : [31, 0, 2],
        'splintmail' : [53, 0, 3],
        'bandedmail' : [75, 0, 4],
        'platemail' : [102, 0, 5]
    },
    'rings' : {
        'd1' : [25, 1, 0],
        'd2' : [50, 2, 0],
        'd3' : [100, 3, 0],
        'p1' : [20, 0, 1],
        'p2' : [40, 0, 2],
        'p3' : [80, 0, 3]
    }
}

hit_points = 100 # 8 for test, 100 for live
# attack 4-8
# armour 0-5
# rings ???

with open('input.txt') as enemy_file:
    values = enemy_file.readlines()

enemy_hit_points = int(values[0].split(':')[1])
enemy_damage = int(values[1].split(':')[1])
enemy_armour = int(values[2].split(':')[1])

def combat_round(hero_hp, hero_d, hero_p, enemy_hp, enemy_d, enemy_p):
    hero_damage = max(hero_d - enemy_p, 1)
    # print('hero damage:', hero_damage)
    enemy_hp -= hero_damage

    if enemy_hp > 0:
        enemy_damage = max(enemy_d - hero_p, 1)
        # print('enemy damage:', enemy_damage)
        hero_hp -= enemy_damage

    return hero_hp, enemy_hp

def cost_equipment(attack, armour, rings=[]):
    if attack < 0 or armour < 0:
        return

    print('costing', attack, armour, rings)

    if ((attack > 8 or armour > 5) and len(rings) == 0) or len(rings) == 0:
        all_rings = list(shop['rings'].keys())
        for ring in all_rings:
            attack_bonus = 0
            armour_bonus = 0
            if ring[0] == 'd':
                attack_bonus += shop['rings'][ring][1]
            else:
                armour_bonus += shop['rings'][ring][2]
            
            yield from cost_equipment(attack-attack_bonus, armour-armour_bonus, [ring])

        import itertools
        for ring_pair in itertools.combinations(all_rings,2):
            ring1 = ring_pair[0]
            ring2 = ring_pair[1]
            attack_bonus = 0
            armour_bonus = 0
            if ring1[0] == 'd':
                attack_bonus += shop['rings'][ring1][1]
            else:
                armour_bonus += shop['rings'][ring1][2]
            if ring2[0] == 'd':
                attack_bonus += shop['rings'][ring2][1]
            else:
                armour_bonus += shop['rings'][ring2][2]
            
            yield from cost_equipment(attack-attack_bonus, armour-armour_bonus, ring_pair)

    total_cost = 0

    attack_cost = None
    for item in shop['weapons'].values():
        if item[1] == attack:
            print('attack', attack, item, 'costs', item[0])
            attack_cost = item[0]

    if attack_cost == None:
        return
    else:
        total_cost += attack_cost

    if armour > 0:
        armour_cost = None
        for item in shop['armour'].values():
            if item[2] == armour:
                print('armour', armour, item, 'costs', item[0])
                armour_cost = item[0]

        if armour_cost == None:
            return
        else:
            total_cost += armour_cost

    for ring in rings:
        print('ring', ring, 'costs', shop['rings'][ring][0])
        total_cost += shop['rings'][ring][0]

    print(attack, armour, rings, 'cost:', total_cost)
    yield total_cost

wins = []
losses = []

for attack in range(4, 15):
    for armour in range(12):
        hero_hp = hit_points
        enemy_hp = enemy_hit_points
        while hero_hp > 0 and enemy_hp > 0:
            hero_hp, enemy_hp = combat_round(hero_hp, attack, armour, enemy_hp, enemy_damage, enemy_armour)

        if hero_hp <= 0:
            # print(f'{attack}, {armour} You died ({hero_hp} vs {enemy_hp})')
            losses.append((attack, armour))
        elif enemy_hp <= 0:
            # print(f'{attack}, {armour} They died ({hero_hp} vs {enemy_hp})')
            wins.append((attack, armour))
        else:
            print('Um... how did we get here?')

#print(wins)
lowest_cost = float('inf')
for attack, armour in wins:
    for cost in cost_equipment(attack, armour):
        if cost and cost < lowest_cost:
            print('*** new lowest', cost, attack, armour)
            lowest_cost = cost
print('lowest win:', lowest_cost)

#print(losses)
highest_cost = 0
costliest = None
for attack, armour in losses:
    for cost in cost_equipment(attack, armour):
        if cost and cost > highest_cost:
            print('*** new highest', cost, attack, armour)
            highest_cost = cost
            costliest = (attack, armour)
print('highest loss:', highest_cost, costliest)

# print(min(list(cost_equipment(5,5))))
