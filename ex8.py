from typing import *

BLACK = 1
WHITE = 0
MAYBE = -1

def turn_to_int(list):
    new_list = []
    for i in list:
        list_ = []
        for j in i:
            list_.append(int(j))
        new_list.append(list_)

    return new_list


def constraint_satisfactions(n, blocks):
    return turn_to_int(test_restriction(all_options(n, blocks, n), blocks))


def minimal_row_length(blocks: List[int]):
    return sum(blocks)+ len(blocks)-1


def check_row_validity(row: List[int], blocks: List[int]):
    if BLACK not in row:
        return True

    black_ind = row.index(BLACK)

    if WHITE not in row[black_ind:]:
        if len(row[black_ind:]) > blocks[0]:
            return False
        else:
            return True

    white_ind = row[black_ind:].index(WHITE)

    if white_ind - black_ind != blocks[0]:
        return False

    return check_row_validity(row[white_ind:], blocks[1:])

def get_options(n, blocks, org_n):
    if n == 0:
        return []

    all_options = []
    for option in get_options(n-1, blocks, org_n):
        for i in range(2):
            added_options = option+[i]
            if check_row_validity(added_options, blocks):
                all_options.append(added_options)

    return all_options




def all_options(n, restriction, org_n) -> List[List[str]]:

    if n == 0:
        return [[]]
    option_list = []
    for option in all_options(n-1, restriction, org_n):
        for i in restriction:
            x = option + ["1"]*i
            if i > 1:
                if len(x) <= org_n:
                    if option == "" or option[-1] == "0":
                        option_list.append(option + "1" * i)
                        if "0" not in option[1:]:
                            break
            else:
                if len(x) <= org_n:
                    if option == "" or option[-1] == "0":
                        option_list.append(option + "1" * i)

        if len(option) == org_n:
            option_list.append(option)
        y = option + "0"
        if len(y) == org_n and "1" not in option:
            continue
        if len(y) <= org_n:
             option_list.append(option + "0")
    return option_list


# def all_options_2(n, blocks: List[int], org_n):
#     if n == 0:
#         return []
#     if sum(blocks) > n:
#         return []
#
#     option_list = []
#     for option in all_options_2(n-1, blocks, org_n):
#         for i in blocks:
#             added = option + [1]*i
#                 if len(added) <= org_n:


# def check_row_validity(row: List[int], blocks: List[int]):
#         if len(blocks) == 0:
#             return 1 not in row
#
#         if 1 not in row or len(row) < blocks[0]:
#             return False
#
#         black_ind = row.index(1)
#         if 0 not in row[black_ind:]:
#             if len(blocks) > 1 or len(row[black_ind:]) != blocks[0]:
#                 return False
#             else:
#                 return True
#
#         white_ind = row[black_ind:].index(0)
#
#         if white_ind - black_ind != blocks[0]:
#             return False
#
#         return check_row_validity(row[white_ind:],blocks[1:])



def try2(row, blocks):


def test_restriction(output_list, restriction):
    new_list = []
    total_res = 0
    for rest in restriction:
        total_res += rest
    for num in output_list:
        for res in restriction:
            if num.count('1') != total_res:
                break
            if '1'*res + "0" != num[:res+1] and "0" + "1"*res != num[-res-1:] and "0" + "1"*res + "0" not in num:
                break
            else:
                if num not in new_list:
                    new_list.append(num)
    return new_list

#print(constraint_satisfactions( 5,[2,2]))

def _row_variations_helper(row, blocks, num_of_row):
    if num_of_row == 0:
        return [""]
    option_list = []
    for option in _row_variations_helper(row, blocks, num_of_row-1):
        for i in blocks:
            x = option + "1" * i
            if i > 1:
                if '1' in option:
                    continue
            if len(x) <= org_n:
                if option == "" or option[-1] == "0":
                    option_list.append(option + "1" * i)
        if len(option) == org_n:
            option_list.append(option)
        y = option + "0"
        if len(y) == org_n and "1" not in option:
            continue
        if len(y) <= org_n:
             option_list.append(option + "0")


    return option_list




def all_options_(n):
    if n == 0:
        return []
    if n == 1:
        return ["0","1"]
    option_list = []
    for option in all_options_(n-1):
        option_list.append(option +"0")
        option_list.append(option + "1")
    return option_list
#print(all_options_(3))


