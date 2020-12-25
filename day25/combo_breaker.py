def loop_size(subject, public):
    val = 1
    loop = 1
    while True:
        val *= subject
        val = val % 20201227
        if val == public:
            return loop
        loop += 1


def encrypt(subject, loop):
    val = 1
    for _ in range(loop):
        val *= subject
        val = val % 20201227
    print('Encryption key: {}'.format(val))
    return val


def get_encryption_key(subject, door_public, key_public):
    door_loop = loop_size(subject, door_public)
    print('Door: public= {}, loops= {}'.format(door_public, door_loop))
    key_loop = loop_size(subject, key_public)
    print('Key: public= {}, loops= {}'.format(key_public, key_loop))

    encryption_key = encrypt(key_public, door_loop)
    encryption_key_check = encrypt(door_public, key_loop)
    assert encryption_key == encryption_key_check
    return encryption_key


if __name__ == '__main__':
    get_encryption_key(7, 17807724, 5764801)

    print('\nMy input')
    get_encryption_key(7, 1526110, 20175123)
