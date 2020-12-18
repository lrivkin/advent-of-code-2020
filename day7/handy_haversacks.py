import re


def parse_input(filename):
    with open(filename) as f:
        rules = f.read().splitlines()
        rule_dict = {}
        for rule in rules:
            bag = rule.split('contain')[0].strip()
            if re.search('no other bags.', rule):
                rule_dict[bag] = ''
                continue
            bag = re.sub(r'bags?.?', '', bag).strip()

            contains = rule.split('contain')[1]
            bag_dict = {}
            for c in contains.split(','):
                c = re.sub(r'bags?.?', '', c).strip()
                label = re.sub(r'[0-9]+', '', c).strip()
                count = re.search(r'[0-9]', c.strip()).group()
                bag_dict[label] = int(count)

            rule_dict[bag] = bag_dict
    return rule_dict


def find_bags_in(bag_dict, bags):
    # Search for all bags that contain at least 1 of the
    #   bags passed in
    can_carry_in = set()
    for label in bag_dict:
        inside = bag_dict[label]
        if any(b in inside for b in bags):
            can_carry_in.add(label)
    return can_carry_in


def run(file, bag):
    bag_dict = parse_input(file)
    del bag_dict[bag]

    can_carry_in = set()
    to_search = {bag}

    while to_search:
        to_search_next = find_bags_in(bag_dict, to_search)
        # print 'searched for {} can carry in {}'.format(to_search, to_search_next)
        can_carry_in.update(to_search_next)

        # Remove the ones you're going to search for from the dictionary
        [bag_dict.pop(b) for b in to_search_next]
        to_search = to_search_next.copy()

    print('This bag ({}) can be carried in {} other bags'.format(bag, len(can_carry_in)))
    return len(can_carry_in)


def count_num_bags_inside(bag_dict, bag):
    this_bag = bag_dict.get(bag, None)
    if not this_bag:
        # This bag has no other bags inside
        return 0

    num_this_bag_can_hold = 0

    for b in this_bag:
        num_b_in_this_bag = this_bag[b]
        # print '{} bag has {} {} bags'.format(bag, b, num_b_in_this_bag)
        num_b_can_hold = count_num_bags_inside(bag_dict, b)
        num_this_bag_can_hold += num_b_in_this_bag * (1 + num_b_can_hold)
    # print '{} bag can overall hold {}'.format(bag, num_this_bag_can_hold)
    return num_this_bag_can_hold


if __name__ == '__main__':
    # Part 1
    assert run('test-input.txt', 'shiny gold') == 4
    run('input.txt', 'shiny gold')

    # Part 2
    assert count_num_bags_inside(parse_input('part2test.txt'), 'shiny gold') == 126
    assert count_num_bags_inside(parse_input('test-input.txt'), 'shiny gold') == 32
    print(count_num_bags_inside(parse_input('input.txt'), 'shiny gold'))
