import re
import numpy
import pprint

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
            tile_store[tile_id] = tile
    print(tiles)
    return tiles


def get_edges(tile):
    tile_rows = tile.splitlines()
    top = tile_rows[0]
    right = ''.join([r[-1] for r in tile_rows])
    bottom = tile_rows[-1][::-1]
    left = ''.join([x[0] for x in reversed(tile_rows)])
    return [top, right, bottom, left]


def reassemble_tiles(tiles):
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
    print('All matches')
    all_matches = {}
    # {1111: {0: (1234, 0), 1: (4567, 2)}}
    for match_list in matches.values():
        for tile_id, edge_id, _ in match_list:
            if tile_id not in all_matches:
                all_matches[tile_id] = {}

    pp.pprint(list(matches.values()))

    no_match = [v[0][0] for v in matches.values() if len(v) == 1 and v[0][2] == 1]
    # matches = {k: v for k, v in matches.items() if len(v) > 1}
    # print('\nThese tiles have edges that line up')
    # pp.pprint(matches)
    # print('\nThese edges need to be on the outside - there is no other edge that matches')
    # pp.pprint(no_match)
    # no_match = [tile_id for tile_id, _, orientation in no_match if orientation == 1]
    print('\nIgnoring reverse orientation, these are the tiles/edges that do not match')
    print(no_match)
    corners = set()
    prod = 1
    for t in no_match:
        if no_match.count(t) > 1:
            if t not in corners:
                corners.add(t)
                prod *= t
    print('Corners {}'.format(corners))
    print('Product of corners: {}\n'.format(prod))


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
    reassemble_tiles(tiles)

    # Real input is a 12 x 12
    tiles = read_tiles('input.txt')
    reassemble_tiles(tiles)

