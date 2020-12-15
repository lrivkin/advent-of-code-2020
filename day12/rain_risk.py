ns = 0
ew = 0
facing = 0


def to_direction(n):
    while n < 0:
        n += 360
    n = n % 360
    if n == 0:
        return 'E'
    if n == 90:
        return 'N'
    if n == 180:
        return 'W'
    if n == 270:
        return 'S'


def move(d):
    global ns, ew, facing
    action = d[0]
    # print('Action: {}'.format(d)
    num = int(d[1:])
    if action in ['L', 'R']:
        if action == 'L':
            facing += num
        else:
            facing -= num
        # print('\tTurned {}{} now facing {}'.format(action, num, to_direction(facing))
        return
    if action == 'F':
        action = '{}{}'.format(to_direction(facing), num)
        # print('\tMoving forward {}'.format(num)
        move(action)
        return

    if action == 'N':
        ns += num
    elif action == 'S':
        ns -= num
    elif action == 'E':
        ew += num
    elif action == 'W':
        ew -= num
    # print('\tN: {} E: {} direction: {}'.format(ns, ew, to_direction(facing))


def run(file):
    with open(file) as f:
        directions = f.read().splitlines()
        for d in directions:
            move(d)
        print('Part 1, searching {}'.format(file))
        print('Final location: N {} E {}'.format(ns, ew))
        print('Cardinal direction: {}\n'.format(abs(ns) + abs(ew)))
        return abs(ns) + abs(ew)


def process_instruction(d, w_ns, w_ew, b_ns, b_ew):
    action = d[0]
    if action == 'F':
        b_ns, b_ew = move_boat(d, w_ns, w_ew, b_ns, b_ew)
    else:
        w_ns, w_ew = move_waypoint(d, w_ns, w_ew)
    # print('Boat position N: {} E: {}, waypoint N:{}, E:{}\n'.format(b_ns, b_ew, w_ns, w_ew)
    return b_ns, b_ew, w_ns, w_ew


def move_boat(d, w_ns, w_ew, b_ns, b_ew):
    # print('Moving boat forward {}'.format(d)
    num = int(d[1:])
    b_ns += num * w_ns
    b_ew += num * w_ew

    # print('New boat position: N{} E{}'.format(b_ns, b_ew)
    return b_ns, b_ew


def move_waypoint(direction, w_ns, w_ew):
    # print('Moving waypoint {}'.format(direction)
    action = direction[0]
    num = int(direction[1:])
    if action in ['L', 'R']:
        if action == 'R':
            # Make the right direction equivalent to L
            num = 360 - num
        while num < 0:
            num += 360
        num = num % 360
        if num == 0:
            return w_ns, w_ew
        if num == 180:
            return -w_ns, -w_ew
        if num == 90:
            return w_ew, -w_ns
        if num == 270:
            return -w_ew, w_ns
    if action == 'N':
        w_ns += num
    elif action == 'S':
        w_ns -= num
    elif action == 'E':
        w_ew += num
    elif action == 'W':
        w_ew -= num
    return w_ns, w_ew


def part2(file):
    boat_n = 0
    boat_e = 0
    way_n = 1
    way_e = 10
    with open(file) as f:
        actions = f.read().splitlines()
        for a in actions:
            new_spots = process_instruction(a, way_n, way_e, boat_n, boat_e)
            boat_n, boat_e, way_n, way_e = new_spots
    print('Part 2, searching {}'.format(file))
    print('Final location: N {} E {}'.format(boat_n, boat_e))
    print('Cardinal direction: {}\n'.format(abs(boat_n) + abs(boat_e)))
    return abs(boat_n) + abs(boat_e)


if __name__ == '__main__':
    assert run('test-input.txt') == 25
    run('input.txt')
    assert part2('test-input.txt') == 286
    part2('input.txt')
