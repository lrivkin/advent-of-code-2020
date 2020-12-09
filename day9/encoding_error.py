def first_invalid(file, preamble):
    with open(file) as f:
        numbers = f.read().splitlines()
        numbers = [int(n) for n in numbers]

        for i in range(len(numbers) - preamble):
            num_to_validate = numbers[i + preamble]
            options = set(numbers[i:i + preamble])
            valid = False
            for o in options:
                target = num_to_validate - o
                if target in options:
                    valid = True
                    break
            if not valid:
                print '{} is invalid'.format(num_to_validate)
                return num_to_validate


def adds_to_invalid(file, invalid_number):
    with open(file) as f:
        numbers = f.read().splitlines()
        numbers = [int(n) for n in numbers]
        low = 0
        high = 1
        while high < len(numbers):
            s = sum(numbers[low:high])
            if s == invalid_number:
                min_in_range = min(numbers[low:high])
                max_in_range = max(numbers[low:high])
                print 'encryption weakness: {} + {} = {}'.format(
                    min_in_range, max_in_range, min_in_range + max_in_range)
                return min_in_range + max_in_range
            elif s < invalid_number:
                high += 1
            elif s > invalid_number:
                low += 1


if __name__ == '__main__':
    print 'Day 9: Encoding Error'
    print '\nPart 1'
    assert first_invalid('test.txt', 5) == 127
    part1 = first_invalid('input.txt', 25)

    print '\nPart 2'
    assert adds_to_invalid('test.txt', 127) == 62
    part2 = adds_to_invalid('input.txt', part1)
