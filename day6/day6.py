def count_anyone(group):
    answers = set()
    for response in group.splitlines():
        answers.update(set(response))
    # print "{}\t{}".format(len(answers),
    #                       group.replace('\n', ', '))
    return len(answers)


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
            anyone += count_anyone(g)
            everyone += count_everyone(g)
        print 'Part 1: Any group member has answer = {}'.format(anyone)
        print 'Part 2: Entire group has answer = {}'.format(everyone)
