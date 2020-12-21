from itertools import product
import copy

check_directions = []


def initialize_grid(z_size, y_size, x_size, placeholder=0):
    # TLDR: using xyz_cube = [list(xy_plane)] ended up as a shallow copy
    # It copied the list but the list inside remained a reference
    # DEEP COPY IS IMPORTANT
    x_row = [placeholder for _ in range(x_size)]
    xy_plane = [list(x_row) for _ in range(y_size)]
    xyz_cube = [copy.deepcopy(xy_plane) for _ in range(z_size)]
    return xyz_cube


def calculate_adjacent_cubes(dimensions=3):
    global check_directions
    check_directions.clear()
    check_directions = list(product([-1, 0, 1], repeat=dimensions))
    self_cube = (0,)*dimensions
    check_directions.remove(self_cube)


def get_from_grid(grid, x, y, z, w=None):
    if w and 0 <= w < len(grid):
        grid = grid[w]
    if 0 <= x < len(grid[0][0]) and 0 <= y < len(grid[0]) and 0 <= z < len(grid):
        return grid[z][y][x]
    return '.'


def count_active_neighbors(grid):
    # Initialize the grid of all the places we want to look at (pad +- 1 of our grid)
    z_len = len(grid)
    y_len = len(grid[0])
    x_len = len(grid[0][0])
    active_grid = initialize_grid(z_len+2, y_len+2, x_len+2, placeholder=0)
    for z in range(z_len):  # 1 layer, z = 0
        for y in range(y_len):  # 3: y = 0-2
            for x in range(x_len):  # 3: x = 0-2
                # If this spot is active, increment the count of all the cubes that touch it
                if get_from_grid(grid, x, y, z) == '#':
                    change_positions = [(z+dz+1, y+dy+1, x+dx+1) for dx, dy, dz in check_directions]
                    for pz, py, px in change_positions:
                        active_grid[pz][py][px] = active_grid[pz][py][px] + 1
    return active_grid


def run_cycle(active_count, grid):
    z_len = len(active_count)
    y_len = len(active_count[0])
    x_len = len(active_count[0][0])
    new_grid = initialize_grid(z_len, y_len, x_len, placeholder='.')
    for z in range(z_len):
        for y in range(y_len):
            for x in range(x_len):
                # the position in this new grid is offset by 1 from the old grid
                current_status = get_from_grid(grid, x - 1, y - 1, z - 1)
                if current_status == '.' and active_count[z][y][x] == 3:
                    new_grid[z][y][x] = '#'
                if current_status == '#' and 1 < active_count[z][y][x] < 4:
                    new_grid[z][y][x] = '#'
    return new_grid


def count_total_active(grid):
    return str(grid).count('#')


def run(file):
    print('Running file {}'.format(file))
    with open(file) as f:
        grid = [f.read().splitlines()]
        calculate_adjacent_cubes()
        for i in range(6):
            active_count = count_active_neighbors(grid)
            grid = run_cycle(active_count, grid)
            print('cycle: {} number active: {}'.format(i+1, count_total_active(grid)))
    print('')


if __name__ == '__main__':
    calculate_adjacent_cubes(3)
    calculate_adjacent_cubes(4)
    print('Day 17: Conway Cubes')
    print('Part 1: 3D cube')
    run('test-input.txt')
    run('input.txt')
