from functools import reduce

tickets = []
my_ticket = []
valid_tickets = []
rules_dict = {}
rule_positions = []


def parse_rules(rules):
    global rules_dict
    for r in rules.splitlines():
        parts = r.split(': ')
        rule = parts[0]
        values = [[int(i2) for i2 in i.split('-')] for i in parts[1].split(' or ')]
        rules_dict[rule] = values
        # values = [i for i in parts.split(' or ')]
    print('all the rules: {}'.format(rules_dict))


def parse_nearby_tickets(nearby):
    tix = nearby.splitlines()[1:]
    global tickets
    tickets = [[int(v) for v in t.split(',')] for t in tix]
    print('nearby tickets: {}'.format(tickets))


def parse_my_ticket(my_ticket_unparsed):
    global my_ticket
    my_ticket = [int(v) for v in my_ticket_unparsed.splitlines()[1].split(',')]
    print('my ticket: {}'.format(my_ticket))


def parse_input(file):
    with open(file) as f:
        sections = f.read().split('\n\n')
    parse_rules(sections[0])
    parse_my_ticket(sections[1])
    parse_nearby_tickets(sections[2])


def find_invalid_tickets():
    total_invalid = 0
    invalid_tickets = [t for t in tickets if t not in valid_tickets]

    ranges = []
    [ranges.extend(r) for r in rules_dict.values()]

    for t in invalid_tickets:
        for value in t:
            is_valid = any([r[0] <= value <= r[1] for r in ranges])
            if not is_valid:
                # print('t: {} bad value'.format(value))
                total_invalid += value
    print('ticket scanning error rate = {}\n'.format(total_invalid))
    return total_invalid


def get_valid_tickets():
    global valid_tickets
    ranges = []
    [ranges.extend(r) for r in rules_dict.values()]

    for t in tickets:
        if all([any([r[0] <= value <= r[1] for r in ranges]) for value in t]):
            valid_tickets.append(t)
    print('valid tickets = {}'.format(valid_tickets))


def discover_fields():
    global rules_dict, rule_positions
    number_fields = len(tickets[0])
    rule_positions = [0] * number_fields

    # position -> all the rules that fit
    possible_fields = []

    for f in range(number_fields):
        rules_for_this_field = set()
        for rule in rules_dict:
            bounds = rules_dict[rule]
            if all([any([b[0] <= v <= b[1] for b in bounds]) for v in [t[f] for t in valid_tickets]]):
                # 'rule' could be in position f
                rules_for_this_field.add(rule)
        possible_fields.append(rules_for_this_field)
    print('fields could go in these positions: {}'.format(possible_fields))

    # go through the list of possible fields and find the final mapping
    num_resolved_fields = 0
    while num_resolved_fields < number_fields:
        # Find the position of the field with only 1 rule left
        one_left = [f for f in possible_fields if len(f) == 1][0]
        field = possible_fields.index(one_left)
        rule = possible_fields[field].pop()
        # Record the spot the rule corresponds to
        rule_positions[field] = rule
        # Clear out this rule from all the other choices
        [rules.discard(rule) for rules in possible_fields]
        num_resolved_fields += 1

    print('fields actually go in these places {}'.format(rule_positions))


def read_my_ticket():
    # rules_we_care_about = []
    rules_we_care_about = [i for i, r in enumerate(rule_positions) if r.startswith('departure')]
    print('these rules matter {}'.format([rule_positions[r] for r in rules_we_care_about]))
    values_we_care_about = [my_ticket[i] for i in rules_we_care_about]
    print('these rules have values: {}'.format(values_we_care_about))
    answer = reduce(lambda x, y: x*y, values_we_care_about)
    print('Final answer = {}'.format(answer))


def run(file, part=1):
    global tickets, valid_tickets, rules_dict, rule_positions
    tickets.clear()
    valid_tickets.clear()
    rules_dict.clear()
    rule_positions.clear()

    parse_input(file)

    get_valid_tickets()
    if part == 1:
        return find_invalid_tickets()
    discover_fields()
    read_my_ticket()


if __name__ == '__main__':
    print('Part 1')
    assert run('test-input.txt', 1) == 71
    run('input.txt')
    print('\nPart 2')
    # run('test-input-2.txt', 2)
    run('input.txt', 2)
