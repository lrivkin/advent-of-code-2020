import re


def get_next_sub_problem(expression):
    if '(' not in expression:
        return None

    r_idx = expression.find(')')
    l_idx = expression[0:r_idx].rfind('(')
    return l_idx, r_idx


def solve_problem(expression, part=1):
    expression = ''.join(re.split('\s', expression))
    print(expression)
    sub_problem = get_next_sub_problem(expression)
    while sub_problem:
        l_idx, r_idx = sub_problem
        if part == 1:
            sub_answer = evaluate(expression[l_idx+1:r_idx])
        else:
            sub_answer = evaluate_addition_first(expression[l_idx+1:r_idx])

        new_expression = '{}{}{}'.format(expression[0:l_idx], sub_answer, expression[r_idx+1:])
        # print('new expression: {}'.format(new_expression))
        expression = new_expression
        sub_problem = get_next_sub_problem(new_expression)

    if part == 1:
        final_answer = evaluate(expression)
    else:
        final_answer = evaluate_addition_first(expression)
    print('\t = {}'.format(final_answer))
    return final_answer


def evaluate(expression):
    # This expression is now just numbers, + and *
    expression = ''.join(expression)
    expression = re.split('(\\*|\\+)', expression)
    answer = int(expression[0])
    for i in range(len(expression[1:])):
        if expression[i] == '+':
            answer += int(expression[i+1])
        elif expression[i] == '*':
            answer *= int(expression[i+1])
        i += 2
    # print('{} = {}'.format(''.join(expression), answer))
    return answer


def evaluate_addition_first(expression):
    # This expression is now just numbers, + and *
    # Do the addition first, THEN multiply
    expression = ''.join(expression)
    expression = re.split('(\\*)', expression)
    new_expression = []
    for piece in expression:
        if '+' in piece:
            added_together = evaluate(piece)
            new_expression.append(str(added_together))
        else:
            new_expression.append(piece)
    return evaluate(new_expression)


if __name__ == '__main__':
    print('Day 18: Operation Order')
    with open('test-input.txt') as f:
        expressions = f.read().splitlines()
        for ex in expressions:
            ex_split = ex.split('=')
            to_eval = ex_split[0]
            expected_answer = ex_split[1]
            assert solve_problem(to_eval) == int(expected_answer)
    with open('input.txt') as f:
        homework = f.read().splitlines()
        homework_sum = 0
        for problem in homework:
            homework_sum += solve_problem(problem)
        print('ALL THE HOMEWORK = {}'.format(homework_sum))

    print('\nPart 2: Math gone CRAZY\n')
    with open('test-input-2.txt') as f:
        expressions = f.read().splitlines()
        for ex in expressions:
            ex_split = ex.split('=')
            to_eval = ex_split[0]
            expected_answer = ex_split[1]
            assert int(expected_answer) == solve_problem(to_eval, 2)

    with open('input.txt') as f:
        homework = f.read().splitlines()
        homework_sum = 0
        for problem in homework:
            homework_sum += solve_problem(problem, 2)
        print('ALL THE HOMEWORK = {}'.format(homework_sum))
