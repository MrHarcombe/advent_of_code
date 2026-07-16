from collections import defaultdict
from io import StringIO

test = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

cookbook = defaultdict(list)
all_ingredients = set()
unmentioned_ingredients = []

# with StringIO(test) as inputs:
with open("input21.txt") as inputs:
    for product in inputs:
        ingredients, allergens = product.split("(")
        ingredient_list = set(ingredients.split())
        all_ingredients.update(ingredient_list)
        unmentioned_ingredients += ingredient_list

        allergen_list = []
        if len(allergens.strip()):
            allergen_list = allergens.strip()[9:-1].split(", ")

        for allergen in allergen_list:
            cookbook[allergen].append(ingredient_list)

for allergen in cookbook:
    if len(cookbook[allergen]):
        cookbook[allergen] = set.intersection(*cookbook[allergen])

for recipe_ingredients in cookbook.values():
    for ingredient in recipe_ingredients:
        while ingredient in unmentioned_ingredients:
            unmentioned_ingredients.remove(ingredient)

print("Part 1:", len(unmentioned_ingredients))

solved = set()
while True:
    singles = [(allergen, ingredient) for (allergen, ingredient) in cookbook.items() if len(ingredient) == 1 and allergen not in solved]
    if len(singles):
        for (allergen, ingredient) in singles:
            solved.add(allergen)
            for recipe_allergen in cookbook:
                if allergen != recipe_allergen:
                    cookbook[recipe_allergen] -= ingredient
    else:
        break

canonicals = sorted(cookbook.items())
canonical_ingredients = []
for allergen in canonicals:
    canonical_ingredients.append("".join(allergen[1]))
    
print("Part 2:", ",".join(canonical_ingredients))
