accumulator = 0
counter = 0


def follow_command(instruction):
    global accumulator, counter
    command, value = instruction
    # print '{}:  {} {}'.format(counter, command, value)
    if command == 'nop':
        counter += 1
    elif command == 'jmp':
        counter += value
    elif command == 'acc':
        accumulator += value
        counter += 1
    return counter


def get_instructions(file):
    with open(file) as f:
        fulltext = f.read()
        lines = fulltext.splitlines()
        return [(l.split()[0], int(l.split()[1])) for l in lines]


def fix_program(file):
    print 'Fixing program {}'.format(file)
    global accumulator, counter
    instructions = get_instructions(file)
    end_of_file = len(instructions)
    for choice in range(end_of_file):
        i2 = list(instructions)
        instruction, value = instructions[choice]
        if instruction == 'jmp':
            i2[choice] = ('nop', value)
        elif instruction == 'nop':
            i2[choice] = ('jmp', value)
        else:
            continue
        run_code(i2)
        if counter == end_of_file:
            print 'changing instruction {}: {} worked'.format(choice, instructions[choice])
            print 'accumulator = {}\n'.format(accumulator)


def run_code(instructions):
    global accumulator, counter
    accumulator = 0
    counter = 0
    visited = set()

    while counter not in visited and counter < len(instructions):
        visited.add(counter)
        instruction = instructions[counter]
        counter = follow_command(instruction)

    return accumulator


if __name__ == '__main__':
    # Part 1: Get the accumulator when the program enters a loop
    assert run_code(get_instructions('p1-test-input.txt')) == 5
    program_loop = run_code(get_instructions('input.txt'))
    print 'Part 1: accumulator = {}'.format(program_loop)

    # Part 2: Brute force which instruction to change
    print '\nPart 2: Finding the broken instruction'
    fix_program('p1-test-input.txt')
    fix_program('input.txt')
