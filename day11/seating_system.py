num_rows = 0
num_cols = 0


def count_visible(board, position, max_depth=None):
    c = position % num_cols
    r = position / num_cols
    directions = [(-1,-1), (-1,0), (-1,+1), (0,-1), (0,+1), (+1,-1), (+1,0), (+1,+1)]

    num_occupied = 0

    for (dr, dc) in directions:
        d = 0   # used to limit how far we search
        r0 = r
        c0 = c
        while 1:
            r0 += dr
            c0 += dc
            if not(0 <= r0 < num_rows and 0 <= c0 < num_cols):
                # We reached the edge of the grid
                break
            if board[r0*num_cols+c0] == 'L':
                break
            if board[r0*num_cols+c0] == '#':
                num_occupied += 1
                break

            if max_depth:
                # Only search x number of chairs around you
                d += 1
                if d == max_depth:
                    break
    return num_occupied


def pretty_print(board, cols):
    chunks = [board[i:i + cols] for i in range(0, len(board), cols)]
    for chunk in chunks:
        print ''.join(chunk)
    print ''


def run(filename, part=1):
    global num_rows, num_cols, board
    with open(filename) as f:
        lines = f.read().splitlines()
        num_rows = len(lines)
        num_cols = len(lines[0].strip())
        # print 'rows: {} cols: {}'.format(num_rows, num_cols)
        # print 'max_position = {}'.format((num_rows-1)*num_cols+num_cols-1)
        board = ''.join(lines)

        min_occupied = 4 if part == 1 else 5
        i = 1
        while 1:
            new_board = list(board)
            calculate_positions_for = [i for i, x in enumerate(new_board) if new_board[i] in ['#', 'L']]
            for p in calculate_positions_for:
                num_occupied = count_visible(board, p, 1) if part == 1 else count_visible(board, p)
                if board[p] == 'L' and num_occupied == 0:
                    new_board[p] = '#'
                elif board[p] == '#' and num_occupied >= min_occupied:
                    new_board[p] = 'L'

            # pretty_print(new_board, num_cols)

            if new_board == board:
                print 'board is stable after {} rounds! {} seats occupied'.format(i, board.count('#'))
                return board.count('#')
                break

            i += 1
            board = list(new_board)


if __name__ == '__main__':
    assert run('testinput.txt') == 37
    run('input.txt')

    assert run('testinput.txt', 2) == 26
    run('input.txt', 2)
