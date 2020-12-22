def play_combat(deck1, deck2):
    while deck1 and deck2:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
    winner = deck1 or deck2
    return winner


def recursive_combat(deck1, deck2):
    game_snapshots = []
    while deck1 and deck2:
        if deck1 in game_snapshots or deck2 in game_snapshots:
            # print('Seen these decks before, player 1 wins')
            return 1, deck1
        game_snapshots.append(deck1[:])

        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            player, _ = recursive_combat(deck1[0:card1], deck2[0:card2])
        else:
            player = 1 if card1 > card2 else 2

        if player == 1:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)

    if deck1:
        # print('Player 1 won this game\nPlayer 1: {}\nPlayer 2: {}\n'.format(deck1, deck2))
        return 1, deck1
    else:
        # print('Player 2 won this game\nPlayer 1: {}\nPlayer 2: {}\n'.format(deck1, deck2))
        return 2, deck2


def calculate_points(winner):
    points = sum([(len(winner)-i)*c for i, c in enumerate(winner)])
    print('Winner got {} points'.format(points))
    return points


def run(file, part=1):
    with open(file) as f:
        players = f.read().split('\n\n')
        player_1 = [int(v) for v in players[0].splitlines()[1:]]
        player_2 = [int(v) for v in players[1].splitlines()[1:]]
        if part == 1:
            winner = play_combat(player_1, player_2)
        else:
            _, winner = recursive_combat(player_1, player_2)
        if player_1:
            print("PLAYER 1 WINS")
        else:
            print("PLAYER 2 WINS")
        print(winner)
        return calculate_points(winner)


if __name__ == '__main__':
    print('Regular Combat!')
    assert run('test-input.txt') == 306
    run('input.txt')

    print('\nRecursive combat!')
    assert run('test-input.txt', 2) == 291
    run('input.txt', 2)
