import re


def parse_rules(raw_rules):
    rules = {}
    for r in raw_rules.splitlines():
        rule_parts = r.split(':')
        rules[rule_parts[0]] = rule_parts[1].strip().strip('"')
    return rules


def get_rule(rules, place):
    rule_0 = rules[place]
    # split on _ to get them separated
    # if there's a |, we want to wrap in ()
    while re.search('[0-9]', rule_0):
        r0 = rule_0.split()

        for i, r in enumerate(r0):
            if re.match('[0-9]+', r):
                new_rule = rules[r]
                # print('{}: {}'.format(r, new_rule))
                if '|' in new_rule:
                    new_rule = '( {} )'.format(new_rule)
                r0[i] = new_rule

        rule_0 = ' '.join(r0)
    # print(''.join(rule_0.split()))
    return ''.join(rule_0.split())


def rule_zero_for_p2(rules, r42, r31, count8, count11):
    rules['8'] = '({})'.format(r42) * count8
    rules['11'] = '({})'.format(r42) * count11 + '({})'.format(r31) * count11
    return get_rule(rules, '0')


def count_new_matches(rules, messages):
    # this is impossible I give up
    rule_42 = get_rule(rules, '42')
    print('42 matches: {}'.format(rule_42))
    rule_31 = get_rule(rules, '31')
    print('31 matches: {}'.format(rule_31))

    # I know the current match using 42 42 31 -> yields a length of 24
    # Max string in our set is length 48
    # Some n number of iterations should work.......?
    matching_message_set = set()
    for count8 in range(1, 6):
        for count11 in range(1, 6):
            rule_0 = rule_zero_for_p2(rules, rule_42, rule_31, count8, count11)
            matching_messages = [m for m in messages if re.fullmatch(rule_0, m)]
            matching_message_set.update(set(matching_messages))
            # print('Finding matches against {}'.format(rule_0))
            print('number matching: {}'.format(len(matching_messages)))
    print('{} messages match'.format(len(matching_message_set)))
    return len(matching_message_set)


def run(file, part=1):
    print('\nRunning Part {}: {}'.format(part, file))
    with open(file) as f:
        sent = f.read().split('\n\n')
        messages = sent[1].splitlines()
        rules = parse_rules(sent[0])
        if part == 2:
            return count_new_matches(rules, messages)

        rule_0 = get_rule(rules, '0')
        print('Finding matches against {}'.format(rule_0))
        num_matches = 0
        for m in messages:
            if re.fullmatch(rule_0, m):
                num_matches += 1
        print('{} messages match'.format(num_matches))
        return num_matches


if __name__ == '__main__':
    print('--- Day 19: Monster Messages ---')
    assert run('test-input.txt') == 2
    run('input.txt')

    assert run('test-input-2.txt', 2) == 12
    run('input.txt', 2)
