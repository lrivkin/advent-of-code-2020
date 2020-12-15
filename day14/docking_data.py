import re
from itertools import chain, combinations

memory = {}


def mask_value(mask, value):
    value_binary = list(format(value, '036b'))
    masked_value_binary = [b if m == 'X' else m for b, m in zip(value_binary, mask)]
    return int(''.join(masked_value_binary), base=2)


def mask_memory_address(mask, location):
    address = list(format(location, '036b'))
    return [b if m == '0' else m for b, m in zip(address, mask)]


def handle_floating_bits(masked_address):
    if 'X' not in masked_address:
        return masked_address
    floating_bits = [i for i, bit in enumerate(masked_address) if bit == 'X']
    floating_bit_powerset = chain.from_iterable(
                                    combinations(floating_bits, r)
                                    for r in range(len(floating_bits) + 1))
    possible_memory_locations = []
    for option in floating_bit_powerset:
        address_binary = ['1' if i in option else bit for i, bit in enumerate(masked_address)]
        address_binary = [bit if bit != 'X' else '0' for bit in address_binary]
        address = int(''.join(address_binary), base=2)
        possible_memory_locations.append(address)
    return possible_memory_locations


def apply_mask(mask, instructions, version=1):
    global memory
    for i in instructions:
        tmp = i.split('=')
        location = int(re.search('[0-9]+', tmp[0]).group())
        value = int(tmp[1])
        if version == 1:
            memory[location] = mask_value(mask, value)
        else:
            masked_address = mask_memory_address(mask, location)
            locations = handle_floating_bits(masked_address)
            for loc in locations:
                memory[loc] = value


def run(file, part=1):
    global memory
    memory.clear()
    with open(file) as f:
        programs = re.split('mask = ', f.read())
        programs = [p for p in programs if p]
        for i, p in enumerate(programs):
            p = p.splitlines()
            mask = list(p[0])
            instructions = p[1:]
            apply_mask(mask, instructions, part)

        # print(memory)
        print('Sum of values = {}'.format(sum(memory.values())))
        return sum(memory.values())


if __name__ == '__main__':
    assert run('test-input.txt') == 165
    run('input.txt')
    assert run('test-input-2.txt', 2) == 208
    run('input.txt', 2)
