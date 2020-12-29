max_cup = 0


def get_destination(current_value, moving):
    destination = current_value - 1
    while 1:
        if destination <= 0:
            destination = max_cup
        if destination not in moving:
            return destination
        destination -= 1


def part2(start):
    global max_cup
    max_cup = 1000000
    turns = 10000000
    # cups will represent the value of the cup
    # the value IN the cup will be the next cup
    start = [int(v) for v in start]
    cups = [0 for _ in range(max_cup+1)]

    curr_cup = start[0]
    cups[-1] = start[0]
    i = 0
    while 1:
        if i == len(start)-1:
            cups[next_val] = i+2
            break
        val = start[i]
        next_val = start[i+1]
        cups[val] = next_val
        i += 1

    for i in range(len(start)+1, max_cup):
        cups[i] = i+1

    # print([(i, cups[i]) for i in range(1, 10)])

    for _ in range(turns):
        n1 = cups[curr_cup]
        n2 = cups[n1]
        n3 = cups[n2]
        dest = get_destination(curr_cup, [n1, n2, n3])
        # print(f'destination: {dest}')

        # destination = 2. 2-> next now = 5
        # after we move.... 2 -> 8 -> 9 -> 1 -> 5
        next_cup = cups[n3]
        cups[curr_cup] = cups[n3]

        cups[n3] = cups[dest]
        cups[dest] = n1

        curr_cup = next_cup
        # print(f'after moving pointing at {next_cup}')
        # print(n1, n2, n3)
        # print([(i, cups[i]) for i in range(1, 10)])

    val1 = cups[1]
    val2 = cups[val1]
    print(val1, val2)
    print(f'multiplied together = {val1*val2}')


def play_game(start):
    global max_cup
    max_cups = len(start)
    turns = 100

    print('Start: {} max_cups={}, turns={}'.format(start, max_cups, turns))

    cups = [int(i) for i in list(start)]
    max_cup = max(cups)
    current_idx = 0
    for move in range(turns):
        current_value = cups[current_idx]
        next_value = cups[(current_idx+4) % max_cups]
        # print('my cup: {}'.format(current_value))
        # print('cups: {}'.format(cups))

        # O(1) to calculate/ get the ones to move
        moving_indices = [(current_idx + i) % len(cups) for i in range(1, 4)]
        moving = [cups[i] for i in moving_indices]
        # print(f'pick up: {moving}')

        # O(N) for each deletion
        for i in sorted(moving_indices, reverse=True):
            del cups[i]

        # O(1)
        destination_val = get_destination(current_value, moving)
        # print(f'destination: {destination_val}')

        # O(N) to search for a value
        destination_idx = cups.index(destination_val)+1

        # Each insert is O(N)
        cups.insert(destination_idx, moving[0])
        cups.insert(destination_idx+1, moving[1])
        cups.insert(destination_idx+2, moving[2])

        # O(N) operation
        current_idx = cups.index(next_value)

    # print('final cups: {}'.format(cups))
    idx_1 = cups.index(1)
    after_1 = cups[idx_1+1:] + cups[:idx_1]
    print('After cup 1: {}\n'.format(''.join([str(i) for i in after_1])))


if __name__ == '__main__':
    print('--- Day 23: Crab Cups ---')
    print('Part 1')
    play_game('389125467')
    play_game('916438275')

    print('\nPart 2')
    print('Test input: 389125467')
    part2('389125467')
    print('\nReal input: 916438275')
    part2('916438275')
