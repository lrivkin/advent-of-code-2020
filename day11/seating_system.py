num_rows = 0
num_cols = 0


def count_occupied(board, position):
    c = position % num_cols
    r = position / num_cols

    # check all (max 8) surrounding spots
    checks = []
    if c > 0 and r > 0:
        checks.append(position - num_cols - 1)
    if r > 0:
        checks.append(position - num_cols)
    if r > 0 and c < num_cols - 1:
        checks.append(position - num_cols + 1)
    if c > 0:
        checks.append(position - 1)
    if c < num_cols - 1:
        checks.append(position + 1)
    if r < num_rows - 1 and c > 0:
        checks.append(position + num_cols - 1)
    if r < num_rows - 1:
        checks.append(position + num_cols)
    if (r < num_rows - 1) and (c < num_cols - 1):
        checks.append(position + num_cols + 1)

    occupied = 0
    for p in checks:
        if board[p] == '#':
            occupied += 1
    return occupied


def pretty_print(board, cols):
    chunks = [board[i:i + cols] for i in range(0, len(board), cols)]
    for chunk in chunks:
        print ''.join(chunk)


def run(filename):
    global num_rows, num_cols, board
    with open(filename) as f:
        lines = f.read().splitlines()
        num_rows = len(lines)
        num_cols = len(lines[0].strip())
        # print 'rows: {} cols: {}'.format(num_rows, num_cols)
        # print 'max_position = {}'.format((num_rows-1)*num_cols+num_cols-1)
        board = ''.join(lines)
        # pretty_print(board, num_cols)

        i = 1
        while 1:
            # print '\nRound {} of musical chairs'.format(i)
            new_board = list(board)
            for p in range(len(board)):
                num_occupied = count_occupied(board, p)
                if board[p] == 'L' and num_occupied == 0:
                    new_board[p] = '#'
                elif board[p] == '#' and num_occupied >= 4:
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
