import re

if __name__ == '__main__':
    with open('testinput.txt') as f:
        rules = f.read().splitlines()
        rule_dict = {}
        for rule in rules:
            bag = rule.split('contain')[0].strip()
            if re.search('no other bags.', rule):
                rule_dict[bag] = ''
                continue

            contains = rule.split('contain')[1]
            bag_dict = {}
            for c in contains.split(','):
                c = re.sub(r'bags?.?', '', c).strip()
                label = re.sub(r'[0-9]+', '', c).strip()
                count = re.search(r'[0-9]', c.strip()).group()
                bag_dict[label] = count

            rule_dict[bag] = bag_dict
    print rule_dict
