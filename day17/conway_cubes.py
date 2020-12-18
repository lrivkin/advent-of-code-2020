check_directions = []


def calculate_adjacent_cubes():
    global check_directions
    check_directions.clear()
    for z in range(-1, 2):
        for y in range(-1, 2):
            for x in range(-1, 2):
                if x == 0 and y == 0 and z == 0:
                    continue
                check_directions.append((x, y, z))


def print_grid(grid):
    for z_slice in range(len(grid)):
        print('z={}'.format(z_slice))
        for y in grid[z_slice]:
            print(''.join(map(str, y)))


def get_from_grid(grid, x, y, z):
    if 0 <= x < len(grid[0][0]) and 0 <= y < len(grid[0]) and 0 <= z < len(grid):
        return grid[z][y][x]
    return '.'


def count_active_neighbors(grid):
    # Initialize the grid of all the places we want to look at (pad +- 1 of our grid)
    active_grid = [[[0 for _ in range(len(grid[0][0]) + 2)] for _ in range((len(grid[0]) + 2))] for _ in range((len(grid) + 2))]
    for z in range(len(grid)):  # 1 layer, z = 0
        for y in range(len(grid[0])):  # 3: y = 0-2
            for x in range(len(grid[0][0])):  # 3: x = 0-2
                # If this spot is active, increment the count of all the cubes that touch it
                if get_from_grid(grid, x, y, z) == '#':
                    change_positions = [(z+dz+1, y+dy+1, x+dx+1) for dx, dy, dz in check_directions]
                    for pz, py, px in change_positions:
                        active_grid[pz][py][px] = active_grid[pz][py][px] + 1
    return active_grid


def run_cycle(active_count, grid):
    new_grid = [[['.' for _ in range(len(active_count[0][0]))] for _ in range((len(active_count[0])))] for _ in range(len(active_count))]
    for z in range(len(active_count)):
        for y in range(len(active_count[0])):
            for x in range(len(active_count[0][0])):
                # the position in this new grid is offset by 1 from the old grid
                current_status = get_from_grid(grid, x - 1, y - 1, z - 1)
                if current_status == '.' and active_count[z][y][x] == 3:
                    new_grid[z][y][x] = '#'
                if current_status == '#' and 1 < active_count[z][y][x] < 4:
                    new_grid[z][y][x] = '#'
    return new_grid


def count_total_active(grid):
    return str(grid).count('#')


def run(file, part=1):
    print('Running file {}'.format(file))
    with open(file) as f:
        grid = [f.read().splitlines()]
        dimensions = 3 if part == 1 else 4
        if dimensions == 4:
            grid = [grid]
        calculate_adjacent_cubes()
        for i in range(6):
            active_count = count_active_neighbors(grid)
            grid = run_cycle(active_count, grid)
            # print_grid(grid)
            print('cycle: {} number active: {}'.format(i+1, count_total_active(grid)))
    print('')


if __name__ == '__main__':
    print('Day 17: Conway Cubes')
    print('Part 1: 3D cube')
    run('test-input.txt')
    run('input.txt')

    # print('\n Part 2: HYPERCUBE')
    # run('test-input.txt', 2)
