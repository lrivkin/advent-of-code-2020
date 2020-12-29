import re
import pprint
from functools import reduce

pp = pprint.PrettyPrinter()
tile_store = {}  # Stored tile_id: tile (as a string)
all_matches = {}  # Stores a map of tile_id : { edge_id : (matching tile) }


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


def generate_matches(tiles):
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


def flip_tile(tile_id, edge):
    """
    Flip the tile vertically or horizontally

    :param tile_id:
    :param edge - we'll flip around this edge:
    """
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
    """
    Rotate the tile by the given factor.
    Update the tile store so the tiles there have the right orientation.
    Update the edge matches map too.

    :param tile_id:
    :param factor:
    :return:
    """
    global tile_store, all_matches

    factor = factor % 4
    if factor == 0:
        return

    matches = all_matches[tile_id]
    tile = tile_store[tile_id].splitlines()
    if factor == 1:
        # print('rotating {} to the right'.format(tile_id))
        rotated = zip(*tile[::-1])
        x = '\n'.join([''.join(list(r)) for r in rotated])
    elif factor == 2:
        # print('rotating {} upside down'.format(tile_id))
        rotated = [t[::-1] for t in tile[::-1]]
        x = '\n'.join([''.join(list(r)) for r in rotated])
    elif factor == 3:
        # print('rotating {} to the left'.format(tile_id))
        rotated = list(zip(*tile))[::-1]
        x = '\n'.join([''.join(list(r)) for r in rotated])

    # After we rotate - each edge needs to change in all_matches to make sure it still points the right way
    # print(matches)
    all_matches[tile_id] = {((k + factor) % 4): v for k, v in matches.items()}
    # print(all_matches[tile_id])
    # print('')
    # print('original    rotated')
    # for i in range(10):
    #     print('  '.join([tile[i], x.splitlines()[i]]))
    # print('')

    tile_store[tile_id] = x


def solve_puzzle():
    square_len = int(pow(len(all_matches), 0.5))
    tile_grid = [[0 for _ in range(square_len)][:] for _ in range(square_len)]

    # Set the first corner (doesn't matter what I pick)
    current_tile = [k for k, v in all_matches.items() if len(v) == 2][0]
    current_target = 1
    current_edges = all_matches[current_tile].keys()
    current_edge = 3 if current_edges == {3, 0} else min(current_edges)
    rotate_tile(current_tile, current_target - current_edge)

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

            # The way the next tile is oriented now, the edge that WILL match is this one
            old_tile_edge = [k for k, v in all_matches[next_tile].items() if v[0] == current_tile][0]

            # 1 = right: match with 3= left     2 = bottom: match with 0 = top
            # This is the way we want that edge of the new tile to be
            target_edge = 3 if current_target == 1 else 0

            rotate_tile(next_tile, target_edge - old_tile_edge)

            # Do we need to flip? they're good if the edges are opposite (we record top -> down or down -> top)
            # There's probably a better way to do this?
            if get_edge(current_tile, current_target) == get_edge(next_tile, target_edge):
                flip_tile(next_tile, target_edge)

            tile_grid[j][i] = next_tile
            current_tile = next_tile if i + 1 < square_len else tile_grid[j][0]

    print('SOLVED THE PUZZLE!!!!')
    pretty_print_tiles(tile_grid)
    check_for_sea_monsters(tile_grid)


monsters = '''
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
'''
monster_regex = monsters.replace(' ', '.').splitlines()
monster_top_regex = re.compile(monster_regex[1])
monster_mid_regex = re.compile(f'(?=({monster_regex[2]}))')
monster_bottom_regex = re.compile(monster_regex[3])
monster_len = len(monster_regex[1])


def get_sea_monsters(image):
    """
    Strategy: Row by row, look for the string that represents
        the middle portion of the monster.
        If it matches, check that the portion above/below also match.
        Monsters CAN overlap.

    :param image - a string representing the image:
    :return num_monsters:
    """
    image_grid = image.splitlines()
    num_monsters = 0
    for i in range(1, len(image_grid) - 1):
        row = image_grid[i]
        if monster_mid_regex.search(row):
            maybe_monsters = [m.span() for m in monster_mid_regex.finditer(row)]
            for start, _ in maybe_monsters:
                if monster_top_regex.match(image_grid[i - 1][start:start+monster_len]) and monster_bottom_regex.match(
                        image_grid[i + 1][start:start+monster_len]):
                    num_monsters += 1
                    # print('MONSTER')
                    # print('\n'.join([image_grid[i + x][start:start+monster_len] for x in range(-1, 2)]))
                    # print('')
    # if num_monsters > 0:
    #     print('')

    return num_monsters


def check_for_sea_monsters(tile_grid):
    """
    Remove the edges from each tile and put them together.
    Flip and rotate the tile until the monsters show up.
    Count the monsters and calculate the answer.

    :param tile_grid:
    :return water roughness:
    """
    image = ''
    for row in tile_grid:
        image_part = [tile_store[t].splitlines() for t in row]
        image = image + '\n'.join([''.join([t[i][1:-1] for t in image_part]) for i in range(1, 9)]) + '\n'

    num_sea_monsters = 0
    for _ in range(4):
        num_sea_monsters = max(num_sea_monsters, get_sea_monsters(image))

        # Check the image flipped vertically + horizontally
        vertical_image = '\n'.join([t[::-1] for t in image.splitlines()])
        num_sea_monsters = max(num_sea_monsters, get_sea_monsters(vertical_image))

        horizontal_image = '\n'.join(image.splitlines()[::-1])
        num_sea_monsters = max(num_sea_monsters, get_sea_monsters(horizontal_image))

        # Rotate the image 1 to the right + check again
        rotated = zip(*image.splitlines()[::-1])
        image = '\n'.join([''.join(list(r)) for r in rotated])

    print("There's {} sea monsters!".format(num_sea_monsters))
    print('Each monster counts for {} #'.format(monsters.count('#')))
    print('There are {} # in the water'.format(image.count('#')))

    roughness = image.count("#") - num_sea_monsters * monsters.count('#')
    print('PART 2: The water has a roughness of {}\n\n'.format(roughness))
    return roughness


def run(file):
    print('RUNNING PROGRAM: ', file)
    tiles = read_tiles(file)
    generate_matches(tiles)

    corners = [k for k, v in all_matches.items() if len(v) == 2]
    prod = reduce(lambda x, y: x * y, corners)
    print('Corners: {}'.format(corners))
    print('PART 1: Product of corners = {}\n'.format(prod))

    solve_puzzle()


if __name__ == '__main__':
    print('--- Day 20: Jurassic Jigsaw ---')
    # Test is only 3 x 3
    run('test-input.txt')

    # Real input is a 12 x 12
    run('input.txt')
