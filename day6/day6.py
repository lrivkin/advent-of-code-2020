def count_anyone(group):
    # remove whitespace + count unique
    group = ''.join(group.split())
    return len(set(group))


def count_everyone(group):
    responses = group.splitlines()
    answers = set(responses.pop())
    for response in responses:
        answers.intersection_update(set(response))
    # print "{}\t{}".format(len(answers),
    #                       group.replace('\n', ', '))
    return len(answers)


if __name__ == '__main__':
    with open('input.txt') as f:
        groups = f.read().split('\n\n')
        anyone = 0
        everyone = 0
        for g in groups:
            anyone += len(set(''.join(g.split())))
            everyone += count_everyone(g)
        print 'Part 1: Any group member has answer = {}'.format(anyone)
        print 'Part 2: Entire group has answer = {}'.format(everyone)
