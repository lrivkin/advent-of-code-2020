def parse_foods(file):
    with open(file) as f:
        foods = f.read().splitlines()
        foods_parsed = {}
        for i, food in enumerate(foods):
            f = food.split('(')
            ingredients = f[0].split()

            allergens = f[1].strip('contains').strip(')')
            allergens = [a.strip() for a in allergens.split(',')]
            foods_parsed[i] = {
                'ingredients': ingredients,
                'allergens': allergens
            }
        return foods_parsed


def get_possible_allergens(foods):
    allergen_to_ingredient = {}
    for food in foods.values():
        ingredients = food['ingredients']

        allergens = food['allergens']
        for a in allergens:
            if a not in allergen_to_ingredient:
                allergen_to_ingredient[a] = set()
            allergen_to_ingredient[a].update(set(ingredients))

    for a in allergen_to_ingredient.keys():
        for food in foods.values():
            ingredients = set(food['ingredients'])

            if a in food['allergens']:
                allergen_to_ingredient[a].intersection_update(ingredients)

    return allergen_to_ingredient


def get_allergens(allergen_to_ingredient):
    print('\nMatching the allergen to their ingredient')
    final_allergen_to_ingredient = {}
    while allergen_to_ingredient:
        # Find the allergen with only 1 possible ingredient
        allergen = [a for a in allergen_to_ingredient if len(allergen_to_ingredient[a]) == 1][0]
        ingredient = allergen_to_ingredient[allergen].pop()
        final_allergen_to_ingredient[allergen] = ingredient
        del allergen_to_ingredient[allergen]
        [allergen_to_ingredient[other_allergen].discard(ingredient) for other_allergen in allergen_to_ingredient]

    print(final_allergen_to_ingredient)
    allergens_list = list(final_allergen_to_ingredient.keys())
    allergens_list.sort()
    print(allergens_list)
    ingredients_list = ','.join([final_allergen_to_ingredient[a] for a in allergens_list])
    print('dangerous list! {}'.format(ingredients_list))
    return ingredients_list


def count_harmless_ingredients(all_ingredients, allergen_to_ingredient):
    print('\nCounting the number of times harmless ingredients are in food')
    not_allergic_ingredients = set(all_ingredients)

    for allergic_ingredient in allergen_to_ingredient.values():
        not_allergic_ingredients.difference_update(allergic_ingredient)
    print('definitely not allergens: {}'.format(not_allergic_ingredients))
    count_not_allergic = sum([all_ingredients.count(n) for n in not_allergic_ingredients])
    print('these non-allergens are in our foods {} times'.format(count_not_allergic))
    return count_not_allergic


def check_label(file, part=1):
    parsed_foods = parse_foods(file)
    allergen_to_ingredient = get_possible_allergens(parsed_foods)
    print('The allergens COULD be in these ingredients: {}'.format(allergen_to_ingredient))

    all_ingredients = [i for ingredients_list in parsed_foods.values() for i in ingredients_list['ingredients']]
    if part == 1:
        return count_harmless_ingredients(all_ingredients, allergen_to_ingredient)
    else:
        return get_allergens(allergen_to_ingredient)


if __name__ == '__main__':
    assert check_label('test-input.txt') == 5
    print('\nReal input')
    check_label('input.txt')

    assert check_label('test-input.txt', 2) == 'mxmxvkd,sqjhc,fvjkl'
    print('\nReal input')
    check_label('input.txt', 2)
