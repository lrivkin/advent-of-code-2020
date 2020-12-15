def process(adapters):
    difference = [adapters[i+1]-adapters[i] for i in range(len(adapters)-1)]
    num_1s = difference.count(1)
    num_3s = difference.count(3)
    print('1: {} 3: {}'.format(num_1s, num_3s))
    return num_1s*num_3s


def count_arrangements(adapters):
    adapters.pop(0)
    num_arrangements = {0: 1}
    for d in adapters:
        n = 0
        options = [d-1, d-2, d-3]
        for o in options:
            n += num_arrangements.get(o, 0)
        num_arrangements[d] = n

    print('There are {} total arrangements'.format(num_arrangements[adapters[-1]]))
    return num_arrangements[adapters[-1]]


def run(file, part):
    with open(file) as f:
        ratings = [int(r) for r in f.readlines()]
        ratings.append(0)
        ratings.append(max(ratings)+3)
        ratings.sort()
        if part == 1:
            return process(ratings)
        else:
            return count_arrangements(ratings)


if __name__ == '__main__':
    assert run('test1.txt', 1) == 35
    assert run('test2.txt', 1) == 22*10
    print(run('input.txt', 1))

    assert run('test1.txt', 2) == 8
    assert run('test2.txt', 2) == 19208
    run('input.txt', 2)
