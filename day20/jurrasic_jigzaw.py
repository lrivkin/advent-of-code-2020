import re
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
    print('')
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

    matches = {k: v for k, v in matches.items() if len(v) > 1}
    print('These tiles have edges that line up')
    pp.pprint(matches)


if __name__ == '__main__':
    print('--- Day 20: Jurassic Jigsaw ---')
    # Test is only 3 x 3
    tiles = read_tiles('test-input.txt')
    reassemble_tiles(tiles)

    # Real input is a 12 x 12
    # tiles = read_tiles('input.txt')
    # reassemble_tiles(tiles)
