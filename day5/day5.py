def locate_seat(partitioning):
    row = [0, 128]
    col = [0, 8]
    for code in partitioning:
        if code == 'F':
            row[1] = row[1] - (row[1] - row[0]) / 2
        elif code == 'B':
            row[0] = row[0] + (row[1] - row[0]) / 2
        elif code == 'L':
            col[1] = col[1] - (col[1] - col[0]) / 2
        elif code == 'R':
            col[0] = col[0] + (col[1] - col[0]) / 2
    row = row[0]
    col = col[0]
    seat_id = row * 8 + col
    # print 'row {}, column {}, seat ID {}'.format(row, col, seat_id)
    return seat_id


def possible_seats():
    rows = range(0, 128)
    columns = range(0, 8)
    all_seats = []
    for c in columns:
        all_seats.extend([r * 8 + c for r in rows])
    return set(all_seats)


def my_seat(taken):
    options = possible_seats() - taken
    leftover = options.copy()

    for s in options:
        # Ignore front/back of the plane
        leftover.discard(s + 1)
        leftover.discard(s - 1)

    return leftover.pop()


if __name__ == '__main__':
    # PART 1 TESTS
    assert locate_seat('FBFBBFFRLR') == 357
    assert locate_seat('BFFFBBFRRR') == 567
    assert locate_seat('FFFBBBFRRR') == 119
    assert locate_seat('BBFFBBFRLL') == 820

    with open('input.txt') as f:
        seats = f.read().splitlines()
        max_id = 0
        seats_taken = set()
        for seat in seats:
            seat_id = locate_seat(seat)
            seats_taken.add(seat_id)
            max_id = max(max_id, seat_id)

        # PART 1
        print 'max seat ID {}'.format(max_id)

        # PART 2
        print my_seat(seats_taken)
