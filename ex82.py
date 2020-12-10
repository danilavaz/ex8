from typing import *

BLACK = 1
WHITE = 0
MAYBE = -1


def check_row_validity(row: List[int], blocks: List[int]):
    if BLACK not in row:
        return True
    black_ind = row.index(BLACK)

    if WHITE in row[black_ind:]:
        white_ind = row[black_ind:].index(WHITE)+black_ind
    else:
        return True

    if white_ind - black_ind != blocks[0]:
        return False

    return check_row_validity(row[white_ind:], blocks[1:])


def get_options(n, blocks, org_n):
    if n == 0:
        return []

    if n == 1:
        return [[WHITE],[BLACK]]

    all_options = []
    for option in get_options(n-1, blocks, org_n):
        for i in range(2):
            added_options = option+[i]
            if len(added_options) == org_n and added_options.count(BLACK) != sum(blocks):
                continue
            if check_row_validity(added_options, blocks):
                all_options.append(added_options)

    return all_options

def constraint_satisfactions(n, blocks):
    return get_options(n, blocks, n)

print(constraint_satisfactions(3,[1]))