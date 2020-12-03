def process_trees(lines, over, down):
    trees = 0
    x = 0
    y = 0
    for l in lines:
        if y % down == 0:
            if l[x] == '#':
                trees += 1
            x = (x + over) % len(l)
        y += 1
    print '({}, {}) total trees: {}'.format(over, down, trees)
    return trees


if __name__ == '__main__':
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    with open('input.txt') as f:
        lines = f.read().splitlines()
        total_trees = [process_trees(lines, over, down) for (over, down) in slopes]
        answer = 1
        for trees in total_trees:
            answer *= trees
        print answer
