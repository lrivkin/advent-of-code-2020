
def validate_by_number(low_count, high_count, key, password):
    key_count = password.count(key)
    return low_count <= key_count <= high_count


def validate_by_position(position_1, position_2, key, password):
    valid_indices = position_1 > 0 and position_2 <= len(password)
    if valid_indices:
        return (password[position_1-1] == key) != (password[position_2-1] == key)
    return False


if __name__ == '__main__':
    part1_total = 0
    part2_total = 0
    with open('input.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            (char_range, key, password) = line.split()
            (num1, num2) = char_range.split('-')
            key = key.strip(':')

            part1 = validate_by_number(int(num1), int(num2), key, password)
            part2 = validate_by_position(int(num1), int(num2), key, password)
            print '{}  p1: {} p2: {}'.format(line, part1, part2)
            if part1:
                part1_total += 1
            if part2:
                part2_total += 1

    print 'part 1: {}'.format(part1_total)
    print 'part 2: {}'.format(part2_total)
