import re
import pprint

pp = pprint.PrettyPrinter()


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

    # print '\nThis bag ({}) can be carried in: {}'.format(bag, can_carry_in)
    print '\nThis bag ({}) can be carried in {} other bags'.format(bag, len(can_carry_in))
    return len(can_carry_in)


if __name__ == '__main__':
    assert run('testinput.txt', 'shiny gold') == 4
    run('input.txt', 'shiny gold')
