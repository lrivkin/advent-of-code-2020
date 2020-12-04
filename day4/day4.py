import re


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
                fields_valid = all([validate_field(field) for field in p.split()])
                if fields_valid or not check_values:
                    valid_count += 1
        return valid_count


def validate_field(field):
    key, value = field.split(':')
    if key == 'byr':
        # return 1920 <= int(value) <= 2002
        return re.match("^(19[2-9][0-9]|200[0-2])$", value)
    if key == 'iyr':
        # return 2010 <= int(value) <= 2020
        return re.match("^(201[0-9]|2020)$", value)
    if key == 'eyr':
        # return 2020 <= int(value) <= 2030
        return re.match("^(202[0-9]|2030)$", value)
    if key == 'hgt':
        if value.endswith('cm'):
            return re.match("^(1[5-8][0-9]|19[0-3])cm$", value)
        if value.endswith('in'):
            return re.match("^(59|6[0-9]|7[0-6])in$", value)
    if key == 'hcl':
        return re.match("^#[0-9a-f]{6}$", value)
    if key == 'ecl':
        return re.match("^(amb|blu|brn|gry|grn|hzl|oth)$", value)
    if key == 'pid':
        return re.match("^[0-9]{9}$", value)
    return key == 'cid'


if __name__ == '__main__':
    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

    # PART 1
    assert parse_passports('p1-test-input.txt', required) == 2
    print 'day 4 part 1: {}'.format(parse_passports('input.txt', required))

    # PART 2
    assert parse_passports('p2-test-valid.txt', required, True) == 4
    assert parse_passports('p2-test-invalid.txt', required, True) == 0
    print 'day 4 part 2: {}'.format(parse_passports('input.txt', required, True))
