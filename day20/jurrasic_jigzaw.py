import re
import pprint
from functools import reduce

pp = pprint.PrettyPrinter()
tile_store = {}     # Make printing/ visualizing easier


def read_tiles(file):
    global tile_store
    tile_store.clear()
    tiles = {}
    with open(file) as f:
        file_lines = f.read().split('\n\n')
        for puzzle in file_lines:
            tile_pieces = re.split("(Tile [0-9]+:\n)", puzzle)
            tile_id = re.search('[0-9]+', tile_pieces[1]).group()
            tile = tile_pieces[2]
            tiles[int(tile_id)] = get_edges(tile)
            tile_store[int(tile_id)] = tile
    print(tiles)
    return tiles


def get_edges(tile):
    tile_rows = tile.splitlines()
    top = tile_rows[0]
    right = ''.join([r[-1] for r in tile_rows])
    bottom = tile_rows[-1][::-1]
    left = ''.join([x[0] for x in reversed(tile_rows)])
    return [top, right, bottom, left]


def parse_tiles(tiles):
    # 1 = original direction
    # -1 means this side was rotated somehow
    matches = {}
    for t in tiles:
        for idx, e in enumerate(tiles[t]):
            if e not in matches:
                matches[e] = []
            matches[e].append((t, idx, 1))

            backwards_e = e[::-1]
            if backwards_e not in matches:
                matches[backwards_e] = []
            matches[backwards_e].append((t, idx, -1))

    # all_matches will be tile_id: {edge: (matching tile/edge)} format
    all_matches = {t: {} for t in tiles}
    for match_list in matches.values():
        a_id, a_edge, a_orientation = match_list[0]
        # Each edge pair will have a +-1 on it, so just look at the +1 orientation
        if a_orientation == 1:
            if len(match_list) > 1:
                b_id, b_edge, b_orientation = match_list[1]
                all_matches[a_id][a_edge] = (b_id, b_edge)
                all_matches[b_id][b_edge] = (a_id, a_edge)

    pp.pprint(all_matches)

    print('\nIgnoring reverse orientation, these are the tiles/edges that do not match')
    corners = [k for k, v in all_matches.items() if len(v) == 2]
    prod = reduce(lambda x, y: x*y, corners)
    print('Corners: {}'.format(corners))
    print('Product of corners: {}\n'.format(prod))

    solve_puzzle(all_matches, corners)
    # edges = [k for k, v in all_matches.items() if len(v) == 3]
    # centers = [k for k, v in all_matches.items() if len(v) == 4]
    # print('Edges: {}'.format(edges))
    # print('Center Pieces: {}'.format(centers))


def flip_tile(tile_id, direction):
    global tile_store

    tile = tile_store[tile_id].splitlines()
    if direction == 1:
        print('flipping {} vertically'.format(tile_id))
        flipped = tile[::-1]
        x = '\n'.join(flipped)
    else:
        print('flipping {} horizontally'.format(tile_id))
        flipped = [t[::-1] for t in tile]
        x = '\n'.join(flipped)

    print('original    flipped')
    for i in range(10):
        print('  '.join([tile[i], x.splitlines()[i]]))
    print('')
    tile_store[tile_id] = x


def rotate_tile(tile_id, factor):
    global tile_store

    factor = factor % 4
    if factor == 0:
        return
    tile = tile_store[tile_id].splitlines()
    if factor == 1:
        print('rotating {} to the right'.format(tile_id))
        rotated = zip(*tile[::-1])
        x = '\n'.join([''.join(list(r)) for r in rotated])
    elif factor == 2:
        print('rotating {} upside down'.format(tile_id))
        rotated = list(zip(*tile[::-1]))[::-1]
        x = '\n'.join([''.join(list(r)) for r in rotated])
    elif factor == 3:
        print('rotating {} to the left'.format(tile_id))
        rotated = list(zip(*tile))[::-1]
        x = '\n'.join([''.join(list(r)) for r in rotated])

    print('original    rotated')
    for i in range(10):
        print('  '.join([tile[i], x.splitlines()[i]]))
    print('')

    tile_store[tile_id] = x


def rotate_corner(corner_id, edge_matches, orientation):
    if edge_matches.keys() == orientation:
        return corner_id, edge_matches
    # both of these could be {0,1}, {1,2}, {2,3}, {3,0}
    edge1 = 3 if orientation == {3, 0} else min(orientation)
    edge2 = (edge1 + 1) % 4

    m1 = 3 if edge_matches.keys() == {3, 0} else min(edge_matches.keys())
    m2 = (m1 + 1) % 4

    # Build the new immediate tile
    new_match = {
        edge1: edge_matches[m1],
        edge2: edge_matches[m2]
    }
    # TEST OUT ROTATION/ FLIPPING:
    rotate_tile(corner_id, 1)
    rotate_tile(corner_id, 2)
    rotate_tile(corner_id, 3)
    flip_tile(corner_id, 1)
    flip_tile(corner_id, -1)
    return corner_id, new_match


def solve_puzzle(match_map, corners):
    num_tiles = len(match_map)
    square_len = int(pow(num_tiles, 0.5))
    tile_grid = [[0 for _ in range(square_len)][:] for _ in range(square_len)]

    match_map_corners = {c: match_map[c] for c in corners}
    # Set the first corner (doesn't matter what I pick)
    top_left_id = corners[0]
    top_left_edges = match_map_corners[top_left_id]
    print(top_left_id, top_left_edges)
    top_left_id, top_left_edges = rotate_corner(top_left_id, top_left_edges, {1, 2})
    print(top_left_id, top_left_edges)


def pretty_print_tiles(tile_ids=[]):
    tile_order = list(tile_store.keys())
    row_len = int(pow(len(tile_order), 0.5))
    tile_size = len(tile_store[tile_order[0]].splitlines())

    tile_grid = [[[] for _ in range(row_len)][:] for _ in range(row_len)]
    for r in range(row_len):
        tile_grid[r] = tile_order[r*row_len:(r+1)*row_len]

    for i, r in enumerate(tile_grid):
        for j, c in enumerate(r):
            tile_grid[i][j] = tile_store[tile_grid[i][j]].splitlines()
    print(tile_grid)

    for r in tile_grid:
        for i in range(tile_size):
            print('  '.join([r[j][i] for j in range(row_len)]))
        print('')


if __name__ == '__main__':
    print('--- Day 20: Jurassic Jigsaw ---')
    # Test is only 3 x 3
    tiles = read_tiles('test-input.txt')
    parse_tiles(tiles)

    # Real input is a 12 x 12
    # tiles = read_tiles('input.txt')
    # parse_tiles(tiles)

