from typing import *

BLACK = 1
WHITE = 0
MAYBE = -1

#   TODO:
#   create recursive function:
#       if count(-1) == 0: run check_row_validity
#           if True, add to list.
#
#       if there is (-1):
#           1. change to 0 and send new list to recursion
#           2. change to 1 and send new list to recursion
#
#       after both options, change back to -1 so we don't change the original
#       list


def row_variations(row: List[int], blocks: List[int]):
    return row_variations_helper(row, blocks, [])


def row_variations_helper(row: List[int], blocks: List[int],
                          variations: List[List[int]]):

    if not is_valid_option(row, blocks):
        return []

    if -1 not in row:
        variations.append(row[:])
        return variations

    ind = row.index(-1)
    for i in range(2):
        row[ind] = i
        row_variations_helper(row, blocks, variations)
    row[ind] = -1
    return variations


def is_valid_option(row: List[int], blocks: List[int]):
    if row.count(MAYBE) == 0:
        return check_row_validity(len(row), row, blocks)

    if row.count(BLACK)+row.count(MAYBE) < sum(blocks) or row.count(BLACK) > sum(blocks):
        return False

    if BLACK not in row:
        if row.count(MAYBE) >= sum(blocks):
            return True
        else:
            return False

    # return True
    # black_ind = row.index(BLACK)
    # if MAYBE in row[black_ind:] or WHITE in row[black_ind:]:
    #     stop_ind = row[black_ind:].index(MAYBE)+black_ind if MAYBE in row[black_ind:] \
    #         else row[black_ind:].index(WHITE)+black_ind
    #     if stop_ind-black_ind > blocks[0]:
    #         return False
    # else:
    #     if len(row[black_ind:]) == blocks[0] and len(blocks) == 1:
    #         return True
    #
    #     return False
    # return True
    #
    # if row[black_ind:].count(BLACK) == len(row[black_ind:]):
    #     if len(row) == blocks[0] and len(blocks) == 1:
    #         return True
    #
    #     return False
    #
    # else:
    #     stop_ind = row[black_ind:].index(MAYBE) if MAYBE in row[black_ind:] \
    #         else row[black_ind:].index(WHITE)
    #     if stop_ind - black_ind > blocks[0]:
    #         return False
    #
    # return True
    #
    # if len(blocks) == 0:
    #     return BLACK not in row
    #
    # if BLACK not in row:
    #     if row.count(MAYBE) >= sum(blocks):
    #         return True
    #     else:
    #         return False
    #
    # black_ind = row.index(BLACK)
    # next_ind = row.index(MAYBE) if MAYBE in row[:black_ind] else black_ind
    # if WHITE in row[next_ind:]:
    #     white_ind = row[next_ind:].index(WHITE) + next_ind
    #     if row[next_ind:white_ind].count(MAYBE) == 0:
    #         if white_ind - next_ind != blocks[0]:
    #             return False
    # else:
    #     if MAYBE in row[next_ind:]:
    #         maybe_ind = row[next_ind:].index(MAYBE) + next_ind
    #         # since we dont have whites. maybe-next is number of blacks between next and maybe
    #         if maybe_ind - next_ind > blocks[0]:
    #             return False
    #
    #         return True
    #
    #     else:
    #         if len(row[black_ind:]) == blocks[0] and len(blocks) == 1:
    #             return True
    #         else:
    #             return False
    #
    # return is_valid_option(row[white_ind:], blocks[1:])





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

print(row_variations([1,1,-1,0],[3]))
print(row_variations([-1,-1,-1,0],[2]))
print(row_variations([-1,0,1,0,-1,0],[1,1]))
print(row_variations([-1,-1,-1],[1]))
print(row_variations([0,0,0],[1]))
print(row_variations([0,0,-1,1,0],[3]))
print(row_variations([0,0,-1,1,0],[2]))
print(row_variations([0,0,1,1,0],[2]))
print(row_variations([-1,-1,-1,0],[1,1]))
