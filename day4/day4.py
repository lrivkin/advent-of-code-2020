import re

validation_schemes = {
    "byr": "^(19[2-9][0-9]|200[0-2])$",
    "iyr": "^(201[0-9]|2020)$",
    "eyr": "^(202[0-9]|2030)$",
    "hgt": "^((1[5-8][0-9]|19[0-3])cm)|((59|6[0-9]|7[0-6])in)$",
    "hcl": "^#[0-9a-f]{6}$",
    "ecl": "^(amb|blu|brn|gry|grn|hzl|oth)$",
    "pid": "^[0-9]{9}$",
    "cid": ""
}

required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}


def parse_passports(filename, required, check_values=False):
    with open(filename) as f:
        passports = f.read().split('\n\n')
        valid_count = 0
        for p in passports:
            # print 'password: {}'.format(p)
            keys = [key.strip(':') for key in re.findall(r"[a-z]{3}:", p)]
            # print keys
            # print required.issubset(set(keys))
            if required.issubset(set(keys)):
                if not check_values:
                    valid_count += 1
                    continue
                if all([validate_field(field) for field in p.split()]):
                    valid_count += 1
        return valid_count


def validate_field(field):
    key, value = field.split(':')
    if key not in validation_schemes:
        return False
    pattern = validation_schemes.get(key)
    return re.match(pattern, value)


if __name__ == '__main__':
    # PART 1
    assert parse_passports('p1-test-input.txt', required) == 2
    print 'day 4 part 1: {}'.format(parse_passports('input.txt', required))

    # PART 2
    assert parse_passports('p2-test-valid.txt', required, True) == 4
    assert parse_passports('p2-test-invalid.txt', required, True) == 0
    print 'day 4 part 2: {}'.format(parse_passports('input.txt', required, True))
