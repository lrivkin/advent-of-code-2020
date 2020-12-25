max_cup = 0
len_cups = 0


def starter_cups(start, total_cups):
    global max_cup, len_cups
    cups = [int(i) for i in list(start)]
    more_cups = total_cups - len(cups)
    next_cup_val = max(cups) + 1
    cups = cups + list(range(next_cup_val, next_cup_val + more_cups))
    max_cup = max(cups)
    len_cups = len(cups)
    return cups


def get_destination(current_value, moving):
    destination = current_value - 1
    while 1:
        if destination <= 0:
            destination = max_cup
        if destination not in moving:
            return destination
        destination -= 1


def play_game(start, part=1):
    max_cups = len(start) if part == 1 else 1000000
    turns = 100 if part == 1 else 10000000
    print('\nStart: {} max_cups={}, turns={}'.format(start, max_cups, turns))

    cups = starter_cups(start, max_cups)
    current_idx = 0
    for move in range(turns):
        if move % 1000 == 0:
            print('Move {}, index: {}'.format(move, current_idx))

        current_value = cups[current_idx]
        next_value = cups[(current_idx+4) % len_cups]
        # print('my cup: {}'.format(current_value))
        # print('cups: {}'.format(cups))

        # next_indices = [(current_idx+1+r) % len_cups for r in range(3)]
        # moving = [cups[i] for i in next_indices]

        # .pop() is O(N-i) -> O(N)
        moving = [cups.pop((current_idx + 1) % len(cups)) for _ in range(3)]

        # print('pick up: {}'.format(moving))

        # O(1)
        destination_val = get_destination(current_value, moving)

        destination_idx = cups.index(destination_val)+1
        # Each insert is O(N)
        cups.insert(destination_idx, moving[0])
        cups.insert(destination_idx+1, moving[1])
        cups.insert(destination_idx+2, moving[2])

        # O(N) operation
        # Would be able to get this down to O(1) with a bit of math which could be good
        current_idx = cups.index(next_value)

    # print('final cups: {}'.format(cups))
    idx_1 = cups.index(1)
    if part == 1:
        after_1 = cups[idx_1+1:] + cups[:idx_1]
        print('After cup 1: {}'.format(''.join([str(i) for i in after_1])))
    else:
        cup_a = cups[(idx_1+1) % len_cups]
        cup_b = cups[(idx_1+2) % len_cups]
        print('Cup 1: {}, Cup 2: {}, multiplied: {}'.format(cup_a, cup_b, cup_a*cup_b))


if __name__ == '__main__':
    print('--- Day 23: Crab Cups ---')
    # play_game('389125467')
    # play_game('916438275')

    play_game('389125467', 2)
