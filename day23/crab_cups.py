def starter_cups(start, total_cups):
    cups = [int(i) for i in list(start)]
    more_cups = total_cups - len(cups)
    next_cup_val = max(cups) + 1
    cups = cups + list(range(next_cup_val, next_cup_val + more_cups))
    # print(cups)
    return cups


def get_destination(cups, current_value):
    # print(cups)
    if current_value < min(cups):
        destination = max(cups)
    else:
        destination = max([c for c in cups if c < current_value])

    # print('destination: {}'.format(destination))
    return destination


def play_game(start, part):
    max_cups = len(start) if part == 1 else 1000000
    turns = 100 if part == 1 else 10000000
    print('\nStart: {} max_cups={}, turns={}'.format(start, max_cups, turns))

    cups = starter_cups(start, max_cups)

    current_idx = 0
    for move in range(turns):
        # print('\nMove {}'.format(move+1))
        current_value = cups[current_idx]
        # print('my cup: {}'.format(current_value))
        # print('cups: {}'.format(cups))

        next_indices = [(current_idx+1+r) % len(cups) for r in range(3)]

        moving = [cups[i] for i in next_indices]
        # print('pick up: {}'.format(moving))

        # Make this better too. Should be able to wrap more easily.
        other_cups = [cups[i] for i in range(len(cups)) if i not in next_indices and i != current_idx]
        destination_val = get_destination(other_cups, current_value)

        # Delete these from current cups? This is bad. Make it better.
        [cups.remove(i) for i in moving]

        destination_idx = cups.index(destination_val)+1

        cups = cups[:destination_idx] + moving + cups[destination_idx:]
        # ALSO BAD: should be able to know where the current index went to!
        current_idx = (cups.index(current_value)+1) % len(cups)

    # print('final cups: {}'.format(cups))
    idx_1 = cups.index(1)
    if part == 1:
        after_1 = cups[idx_1+1:] + cups[:idx_1]
        print('After cup 1: {}'.format(''.join([str(i) for i in after_1])))
    else:
        cup_a = cups[(idx_1+1) % len(cups)]
        cup_b = cups[(idx_1+2) % len(cups)]
        print('Cup 1: {}, Cup 2: {}, multiplied: {}'.format(cup_a, cup_b, cup_a*cup_b))


if __name__ == '__main__':
    print('--- Day 23: Crab Cups ---')
    # play_game('389125467')
    # play_game('916438275')

    play_game('389125467', 2)
