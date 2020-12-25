import re
tile_store = {}     # Make printing/ visualizing easier


def read_tiles(file):
    global tile_store
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
    # print('top: {}'.format(top))
    right = ''.join([r[-1] for r in tile_rows])
    # print('right: {}'.format(right))
    bottom = tile_rows[-1][::-1]
    # print('bottom: {}'.format(bottom))
    left = ''.join([x[0] for x in reversed(tile_rows)])
    # print('left: {}'.format(left))
    return [top, right, bottom, left]


if __name__ == '__main__':
    print('--- Day 20: Jurassic Jigsaw ---')
    read_tiles('test-input.txt')
