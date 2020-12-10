from typing import *

BLACK = 1
WHITE = 0
MAYBE = -1


def check_row_validity(n: int, row: List[int], blocks: List[int]):
    if len(row) == n and row.count(BLACK) != sum(blocks):
        return False

    if BLACK not in row:
        return True
    black_ind = row.index(BLACK)

    if WHITE in row[black_ind:]:
        white_ind = row[black_ind:].index(WHITE) + black_ind
    else:
        if len(row[black_ind:]) > blocks[0]:
            return False
        else:
            return True

    if white_ind - black_ind != blocks[0]:
        return False

    return check_row_validity(n, row[white_ind:], blocks[1:])


def get_options(n, blocks, org_n):
    if n == 0:
        return []

    if n == 1:
        return [[WHITE],[BLACK]]

    all_options = []
    for option in get_options(n-1, blocks, org_n):
        for i in range(2):
            added_options = option+[i]
            if check_row_validity(org_n, added_options, blocks):
                all_options.append(added_options)

    return all_options


def constraint_satisfactions(n, blocks):
    return get_options(n, blocks, n)


print(constraint_satisfactions(16,[2,3,1,1,4]))
