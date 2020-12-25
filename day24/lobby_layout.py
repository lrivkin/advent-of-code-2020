"""
COORDINATE SYSTEM: +-x goes along the SE/ NW line
                   +-y goes along the NE/ SW line

For moving (p1) to get E or W you need to combine 1 moves
    E = move SE then NE = (1, 1)
    W = move NW then SW = (-1, -1)

These would all be adjacent to (0, 0):
    E: (1,1)
    SE: (1, 0)
    SW: (0, -1)
    W: (-1, -1)
    NW: (-1, 0)
    NE: (0, 1)
"""
import re


tiles_around = [(1, 0), (0, -1), (-1, -1), (-1, 0), (0, 1), (1, 1)]


def find_tile(directions):
    location = [0, 0]
    # print('moving tile: {}'.format(directions))
    for d in directions:
        if d == 'e':
            location[0] += 1
            location[1] += 1
        elif d == 'w':
            location[0] -= 1
            location[1] -= 1
        elif d == 'se':
            location[0] += 1
        elif d == 'nw':
            location[0] -= 1
        elif d == 'sw':
            location[1] -= 1
        elif d == 'ne':
            location[1] += 1

    # print('tile at location: {}'.format((location[0], location[1])))
    return location[0], location[1]


def adjacent_tiles(tile):
    se, ne = tile
    touching_tiles = [(se+d_se, ne+d_ne) for d_se, d_ne in tiles_around]
    return touching_tiles


def count_adjacent_black_tiles(current_state):
    current_counts = {}
    for tile in current_state:
        # print('tile: {}'.format(tile))
        adjacent = adjacent_tiles(tile)
        for a in adjacent:
            if a not in current_counts:
                current_counts[a] = 0
            current_counts[a] += 1
            # print('{}: {}'.format(a, current_counts[a]))
        # print('\t{}'.format(current_counts))
    return current_counts


def flip_tiles(current_black_tiles):
    """
    Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
    """
    adjacent = count_adjacent_black_tiles(current_black_tiles)
    next_day_black_tiles = set()

    for tile in adjacent:
        if tile in current_black_tiles and 0 < adjacent[tile] < 3:
            next_day_black_tiles.add(tile)
        elif adjacent[tile] == 2:
            next_day_black_tiles.add(tile)
    return next_day_black_tiles


def run_art_exhibit(initial_tiles):
    print('Changing the tiles day by day')
    tiles = initial_tiles
    for i in range(100):
        tiles = flip_tiles(tiles)
        if (i+1) % 10 == 0:
            print('Day {}: {}'.format(i+1, len(tiles)))
    return len(tiles)


def run(file, part=1):
    print('Running {}'.format(file))
    with open(file) as f:
        black_tiles = set()

        for d in f.read().splitlines():
            d = [r for r in re.split('(ne)|(se)|(nw)|(sw)|(e)|(w)', d) if r]
            tile_to_flip = find_tile(d)
            if tile_to_flip in black_tiles:
                # print('flip {} back to white'.format(tile_to_flip))
                black_tiles.remove(tile_to_flip)
            else:
                # print('flip {} to black'.format(tile_to_flip))
                black_tiles.add(tile_to_flip)
        # print(black_tiles)
        print('There are {} tiles black side up\n'.format(len(black_tiles)))
        if part == 1:
            return len(black_tiles)

        return run_art_exhibit(black_tiles)


if __name__ == '__main__':
    print('--- Day 24: Lobby Layout ---')
    # Tests for the tile location util
    assert find_tile(['e', 'se', 'w']) == (1, 0)    # end 1 spot SE
    assert find_tile(['nw', 'w', 'sw', 'e', 'e']) == (0, 0)     # end back at same spot

    # Part 1: Count of flipped tiles
    assert run('test-input.txt') == 10
    run('input.txt')

    # Part 2: Change the tiles each day
    assert run('test-input.txt', 2) == 2208
    run('input.txt', 2)
