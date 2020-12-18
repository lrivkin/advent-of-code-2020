import re


def parse_expression(expression):
    # get rid of whitespace
    expression = ''.join(re.split('\s', expression))
    print(expression)

    pairs = []
    lefts = []
    for i, c in enumerate(expression):
        if c == '(':
            lefts.append(i)
        if c == ')':
            pairs.append((lefts.pop(), i))
            # evaluate between these 2 indices
            # stick the result somewhere?
    print(pairs)


def evaluate(expression):
    # Assume this section has already been stripped down of all () and just evaluate it
    expression = ''.join(re.split('\s', expression))
    expression = re.split('(\\*|\\+)', expression)
    print(expression)
    answer = int(expression[0])
    for i in range(len(expression[1:])):
        if expression[i] == '+':
            answer += int(expression[i+1])
        elif expression[i] == '*':
            answer *= int(expression[i+1])
        i += 2
    print(answer)
    return answer


if __name__ == '__main__':
    # print('Day 18: Operation Order')
    # evaluate('1 + 2 * 3 + 4 * 5 + 6')
    with open('test-input.txt') as f:
        expressions = f.read().splitlines()
        for ex in expressions:
            ex_split = ex.split('=')
            to_eval = ex_split[0]
            expected_answer = ex_split[1]
            # print('evaluate {}'.format(to_eval))
            # print('equals {}'.format(expected_answer))
            parse_expression(to_eval)
            print('')
