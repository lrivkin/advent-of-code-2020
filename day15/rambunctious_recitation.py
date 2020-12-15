def word_spoken(starting_numbers, turns=2020):
    # Nothing about this is efficient or pythonic
    history = {}
    turn = 1

    for s in starting_numbers[:-1]:
        # print('Turn {} spoke {}'.format(turn, s))
        history[s] = turn
        turn += 1

    last_num = starting_numbers[-1]
    while turn < turns:
        if last_num in history:
            next_num = turn - history[last_num]
        else:
            next_num = 0
        history[last_num] = turn
        # print('Turn {} spoke {}'.format(turn, last_num))
        last_num = next_num
        turn += 1

    print('Puzzle {}: {}'.format(starting_numbers, last_num))
    return last_num


if __name__ == '__main__':
    print('Day 15')
    # Part 1
    assert word_spoken([0, 3, 6]) == 436
    assert word_spoken([1, 3, 2]) == 1
    assert word_spoken([2, 1, 3]) == 10
    assert word_spoken([1, 2, 3]) == 27
    assert word_spoken([2, 3, 1]) == 78
    assert word_spoken([3, 2, 1]) == 438
    assert word_spoken([3, 1, 2]) == 1836
    word_spoken([1, 0, 18, 10, 19, 6])

    # Part 2
    word_spoken([1, 0, 18, 10, 19, 6], 30000000)
