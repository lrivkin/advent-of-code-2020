from helpers import combine_phased_rotations


def find_earliest(busses, earliest_time):
    best_times = [(earliest_time / b + 1) * b for b in busses]
    min_time = min(best_times)
    bus = busses[best_times.index(min_time)]
    for b, t in zip(busses, best_times):
        print 'Bus {} best time {}'.format(b, t)
    return bus, min_time


def find_subsequent_schedule(bus_list):
    busses = []
    for i, bus in enumerate(bus_list):
        if bus != 'x':
            busses.append((int(bus), i))

    # Bus offset to deal with
    combined_period, combined_offset = busses[0]
    print 'First bus {}, {}'.format(combined_period, combined_offset)

    for i in range(1, len(busses)):
        bus, offset = busses[i]
        combined_period, combined_offset = combine_phased_rotations(combined_period, combined_offset, bus, -offset)
        print 'First place {} overlaps with others is {}'.format(bus, combined_offset)

    print 'Earliest time to leave is {}\n'.format(combined_offset)
    return combined_offset


def run(filename, part=1):
    with open(filename) as f:
        lines = f.read().splitlines()
        earliest_time = int(lines[0])
        if part == 1:
            busses = [int(b) for b in lines[1].split(',') if b != 'x']
            bus, time = find_earliest(busses, earliest_time)

            print 'Take bus {} at time {}\n'.format(bus, time)
            return bus * (time - earliest_time)
        else:
            busses = [b for b in lines[1].split(',')]
            return find_subsequent_schedule(busses)


if __name__ == '__main__':
    assert run('test-input.txt') == 295
    print run('input.txt')

    assert find_subsequent_schedule([17, 'x', 13, 19]) == 3417
    assert find_subsequent_schedule([67, 7, 59, 61]) == 754018
    assert find_subsequent_schedule([67, 'x', 7, 59, 61]) == 779210
    assert find_subsequent_schedule([67, 7, 'x', 59, 61]) == 1261476
    assert find_subsequent_schedule([1789, 37, 47, 1889]) == 1202161486
    assert run('test-input.txt', 2) == 1068781
    run('input.txt', 2)

