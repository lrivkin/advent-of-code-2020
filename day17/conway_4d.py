import copy

check_directions = []


def calculate_adjacent_cubes():
    global check_directions
    check_directions.clear()
    for z in range(-1, 2):
        for y in range(-1, 2):
            for x in range(-1, 2):
                for w in range(-1, 2):
                    if w == 0 and x == 0 and y == 0 and z == 0:
                        continue
                    check_directions.append((w, x, y, z))


def get_from_grid(grid, w, x, y, z):
    if 0 <= w < len(grid[0][0][0]) and 0 <= x < len(grid[0][0]) and 0 <= y < len(grid[0]) and 0 <= z < len(grid):
        return grid[z][y][x][w]
    return '.'



def count_active_neighbors(grid):
    z_size = len(grid)
    y_size = len(grid[0])
    x_size = len(grid[0][0])
    w_size = len(grid[0][0][0])
    # Pad our grid of new spots to explore with +- 1 on either side
    active_grid = initialize_grid(z_size+2, y_size+2, x_size+2, w_size+2, 0)
    # print(active_grid)
    for z in range(z_size):
        for y in range(y_size):
            for x in range(x_size):
                for w in range(w_size):
                    # If this spot is active, increment the count of all the cubes that touch it
                    if get_from_grid(grid, w, x, y, z) == '#':
                        change_positions = [(z+dz+1, y+dy+1, x+dx+1, w+dw+1) for dw, dx, dy, dz in check_directions]
                        for pz, py, px, pw in change_positions:
                            active_grid[pz][py][px][pw] = active_grid[pz][py][px][pw] + 1
                        # print(active_grid)
                        # print('active spot at: {}'.format((w, x, y, z)))
                        # print(active_grid)
    # print('after all updates')
    # print(active_grid)
    return active_grid


def run_cycle(active_count, grid):
    z_size = len(active_count)
    y_size = len(active_count[0])
    x_size = len(active_count[0][0])
    w_size = len(active_count[0][0][0])
    new_grid = initialize_grid(z_size, y_size, x_size, w_size, '.')
    for z in range(z_size):
        for y in range(y_size):
            for x in range(x_size):
                for w in range(w_size):
                    # the position in this new grid is offset by 1 from the old grid
                    current_status = get_from_grid(grid, w-1, x - 1, y - 1, z - 1)
                    if current_status == '.' and active_count[z][y][x][w] == 3:
                        new_grid[z][y][x][w] = '#'
                    if current_status == '#' and 1 < active_count[z][y][x][w] < 4:
                        new_grid[z][y][x][w] = '#'
    return new_grid


def count_total_active(grid):
    return str(grid).count('#')


def run(file):
    print('Running file {}'.format(file))
    with open(file) as f:
        grid = [[f.read().splitlines()]]
        calculate_adjacent_cubes()
        for i in range(6):
            active_count = count_active_neighbors(grid)
            grid = run_cycle(active_count, grid)
            print('cycle: {} number active: {}'.format(i+1, count_total_active(grid)))
    print('')


if __name__ == '__main__':
    print('Day 17: Conway Cubes')

    print('\n Part 2: HYPERCUBE')
    run('test-input.txt')
    run('input.txt')
