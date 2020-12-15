import re

memory = {}


def apply_mask(mask, instructions):
    global memory
    for i in instructions:
        tmp = i.split('=')
        location = int(re.search('[0-9]+', tmp[0]).group())
        value = int(tmp[1])
        value_bin = list(format(value, '036b'))
        # print(''.join(value_bin), value)

        for i3, m in enumerate(mask):
            if m != 'X':
                value_bin[i3] = m
        new_value = int(''.join(value_bin), base=2)
        # print(''.join(value_bin), new_value)

        memory[location] = new_value


def run(file):
    global memory
    memory.clear()
    with open(file) as f:
        programs = re.split('mask = ', f.read())
        programs = [p for p in programs if p]
        for i, p in enumerate(programs):
            p = p.splitlines()
            mask = list(p[0])
            instructions = p[1:]
            apply_mask(mask, instructions)

        print(memory)
        print('Sum of values = {}'.format(sum(memory.values())))
        return sum(memory.values())


if __name__ == '__main__':
    assert run('test-input.txt') == 165
    run('input.txt')
