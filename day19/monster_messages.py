import re


def parse_rules(raw_rules):
    rules = {}
    for r in raw_rules.splitlines():
        rule_parts = r.split(':')
        rules[rule_parts[0]] = rule_parts[1].strip().strip('"')
    return rules


def update_for_part2(rules):
    rules['8'] = '42 | 42 8'
    rules['11'] = '42 31 | 42 11 31'
    return rules


def get_rule_0(rules):
    limit = 9
    rule_0 = rules['0']
    # split on _ to get them separated
    # if there's a |, we want to wrap in ()
    while re.search('[0-9]', rule_0) and limit > 0:
        r0 = rule_0.split()

        for i, r in enumerate(r0):
            if re.match('[0-9]+', r):
                new_rule = rules[r]
                # print('{}: {}'.format(r, new_rule))
                if '|' in new_rule:
                    new_rule = '( {} )'.format(new_rule)
                r0[i] = new_rule

        rule_0 = ' '.join(r0)
        limit -= 1
    return ''.join(rule_0.split())


def run(file, part=1):
    print('\nRunning {}'.format(file))
    with open(file) as f:
        sent = f.read().split('\n\n')
        rules = parse_rules(sent[0])
        if part == 2:
            # this is impossible I give up
            rules = update_for_part2(rules)

        rule_0 = get_rule_0(rules)
        print('Finding matches against {}'.format(rule_0))
        messages = sent[1]
        num_matches = 0
        for m in messages.splitlines():
            if re.fullmatch(rule_0, m):
                # print('{} matches!'.format(m))
                num_matches += 1
        print('{} messages match'.format(num_matches))
        return num_matches


if __name__ == '__main__':
    print('--- Day 19: Monster Messages ---')
    assert run('test-input.txt') == 2
    run('input.txt')
