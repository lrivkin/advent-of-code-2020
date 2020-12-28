import re
import pprint
from functools import reduce

pp = pprint.PrettyPrinter()
tile_store = {}     # Stored tile_id: tile (as a string)
all_matches = {}    # Stores a map of tile_id : { edge_id : (matching tile) }


def pretty_print_tiles(tile_ids):
    # assume tile_ids is a [[p1, p2, p3], [p4, p5, p6], ...]
    for row in tile_ids:
        if sum(row) > 0:
            printable_grid = [tile_store[t].splitlines() for t in row if t]
            print('  '.join(['Tile {}:'.format(t) for t in row]))
            for i in range(10):
                print('  '.join([t[i] for t in printable_grid]))
        print('')


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
    # pp.pprint(tiles)
    return tiles


def get_edges(tile):
    tile_rows = tile.splitlines()
    top = tile_rows[0]
    right = ''.join([r[-1] for r in tile_rows])
    bottom = tile_rows[-1][::-1]
    left = ''.join([x[0] for x in reversed(tile_rows)])
    return [top, right, bottom, left]


def get_edge(tile_id, edge):
    edges = get_edges(tile_store[tile_id])
    return edges[edge]


def parse_tiles(tiles):
    global all_matches
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
                # If b_orientation also = +1, we'll have to flip it
                # otherwise, these will match when we finally rotate it right
                b_id, b_edge, _ = match_list[1]
                all_matches[a_id][a_edge] = (b_id, b_edge)
                all_matches[b_id][b_edge] = (a_id, a_edge)

    # pp.pprint(all_matches)

    corners = [k for k, v in all_matches.items() if len(v) == 2]
    prod = reduce(lambda x, y: x*y, corners)
    print('Corners: {}'.format(corners))
    print('Product of corners: {}\n'.format(prod))

    solve_puzzle(all_matches, corners)


def flip_tile(tile_id, edge):
    global tile_store, all_matches

    tile = tile_store[tile_id].splitlines()
    matches = all_matches[tile_id]
    # print('starting: {}'.format(all_matches[tile_id]))
    if edge % 2 != 0:
        # print('flipping {} vertically'.format(tile_id))
        flipped = tile[::-1]
        x = '\n'.join(flipped)
        # Change the even indices - leave the odd ones the same
        all_matches[tile_id] = {k if (k % 2 != 0) else ((k + 2) % 4): v for k, v in matches.items()}
    else:
        # print('flipping {} horizontally'.format(tile_id))
        flipped = [t[::-1] for t in tile]
        x = '\n'.join(flipped)
        # Change the odd indices - leave the even ones the same
        all_matches[tile_id] = {k if (k % 2 == 0) else ((k + 2) % 4): v for k, v in matches.items()}
    # print('ending: {}'.format(all_matches[tile_id]))

    # print('original    flipped')
    # for i in range(10):
    #     print('  '.join([tile[i], x.splitlines()[i]]))
    # print('')
    tile_store[tile_id] = x


def rotate_tile(tile_id, factor):
    global tile_store, all_matches

    factor = factor % 4
    if factor == 0:
        return

    matches = all_matches[tile_id]
    # print(matches)
    tile = tile_store[tile_id].splitlines()
    if factor == 1:
        # print('rotating {} to the right'.format(tile_id))
        rotated = zip(*tile[::-1])
        x = '\n'.join([''.join(list(r)) for r in rotated])
    elif factor == 2:
        # print('rotating {} upside down'.format(tile_id))
        # Flip vertically and flip horizontally = a rotation by 2
        rotated = [t[::-1] for t in tile[::-1]]
        x = '\n'.join([''.join(list(r)) for r in rotated])
    elif factor == 3:
        # print('rotating {} to the left'.format(tile_id))
        rotated = list(zip(*tile))[::-1]
        x = '\n'.join([''.join(list(r)) for r in rotated])

    # After we rotate - each edge needs to change in all_matches to make sure it still points the right way
    all_matches[tile_id] = {((k + factor) % 4): v for k, v in matches.items()}
    # print(all_matches[tile_id])
    # print('')
    # print('original    rotated')
    # for i in range(10):
    #     print('  '.join([tile[i], x.splitlines()[i]]))
    # print('')

    tile_store[tile_id] = x
    return tile_id, get_edges(x)


def solve_puzzle(match_map, corners):
    num_tiles = len(match_map)
    square_len = int(pow(num_tiles, 0.5))
    tile_grid = [[0 for _ in range(square_len)][:] for _ in range(square_len)]

    # Set the first corner (doesn't matter what I pick)
    current_tile = corners[0]
    current_target = 1
    current_edges = all_matches[current_tile].keys()
    current_edge = 3 if current_edges == {3, 0} else min(current_edges)
    rotate_tile(current_tile, current_target-current_edge)

    tile_grid[0][0] = current_tile
    for j in range(square_len):
        for i in range(square_len):
            if i == 0 and j == 0:
                # This is the first corner - we've already placed it
                continue

            # On the first tile of the row: current_target = 2 since we need to match the
            #   bottom edge to the top edge of the next tile
            # Otherwise, current_target = 1 since we match the right edge to the left
            current_target = 1 if i > 0 else 2
            next_tile, next_edge = all_matches[current_tile][current_target]
            old_tile_edge = [k for k, v in all_matches[next_tile].items() if v[0] == current_tile][0]

            # 1 = right: match with 3= left     2 = bottom: match with 0 = top
            target_edge = 3 if current_target == 1 else 0

            rotate_tile(next_tile, target_edge-old_tile_edge)

            # Do we need to flip? they're good if the edges are opposite (we record top -> down or down -> top)
            # There's probably a better way to do this (before I recorded direction of the edge) but ?
            if get_edge(current_tile, current_target) == get_edge(next_tile, target_edge):
                flip_tile(next_tile, target_edge)

            tile_grid[j][i] = next_tile
            current_tile = next_tile if i+1 < square_len else tile_grid[j][0]

    print('SOLVED THE PUZZLE!!!!')
    pretty_print_tiles(tile_grid)


if __name__ == '__main__':
    print('--- Day 20: Jurassic Jigsaw ---')
    # Test is only 3 x 3
    tiles = read_tiles('test-input.txt')
    parse_tiles(tiles)

    # Real input is a 12 x 12
    tiles = read_tiles('input.txt')
    parse_tiles(tiles)
