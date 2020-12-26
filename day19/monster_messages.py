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


def find_max_repeats(messages, rule_42, rule_31):
    # Max string in our set is length 96
    longest_message = max(messages, key=len)
    print('Longest message is length {}:  {}'.format(len(longest_message), longest_message))

    # Pattern 42 + Pattern  31 both match strings of length 8 (real input)
    for m in messages:
        match_42 = re.match(rule_42, m)
        match_31 = re.search(rule_31, m)
        if match_42 and match_31:
            match_42 = len(match_42.group())
            match_31 = len(match_31.group())
            break

    # Worst-case: rule 8 is 1 repeat of 42 (len 8), and rule 11 is (96-8)/(8+8) repeats of rule 42/31
    # Therefore - most times we need to repeat is (96-8)/16
    worst_case = (len(longest_message)-match_42)/(match_42+match_31)
    print('Worst case: rule 11 repeats {}'.format(worst_case))
    return int(worst_case)


def rule_zero_for_p2(r42, r31, count):
    rule8 = '({})+'.format(r42)
    rule11 = '({}){{{}}}({}){{{}}}'.format(r42, count, r31, count)
    return '^{}{}$'.format(rule8, rule11)


def count_new_matches(rules, messages):
    # this is impossible I give up
    rule_42 = get_rule(rules, '42')
    print('42 matches: {}'.format(rule_42))
    rule_31 = get_rule(rules, '31')
    print('31 matches: {}'.format(rule_31))

    max_repeats = find_max_repeats(messages, rule_42, rule_31)
    matching_message_set = set()

    for i in range(max_repeats):
        rule_0 = rule_zero_for_p2(rule_42, rule_31, i+1)
        matching_messages = [m for m in messages if re.match(rule_0, m)]
        matching_message_set.update(set(matching_messages))
        print('Finding matches for rule 31 repeated {} times'.format(i+1))
        print('\t{} messages match'.format(len(matching_messages)))
    print('{} messages match in total'.format(len(matching_message_set)))
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
