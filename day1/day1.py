def find_match(options, target):
    for n1 in options:
        for n2 in options:
            for n3 in options:
                if n1 + n2 + n3 == target:
                    print(n1, n2, n3, n1+n2+n3)
                    return n1*n2*n3


if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.read().splitlines()
        numbers = [int(num) for num in lines]
        print(find_match(numbers, 2020))
