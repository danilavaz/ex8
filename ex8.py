

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

def all_options(n, restriction, org_n):

    if n == 0:
        return [""]
    option_list = []
    for option in all_options(n-1, restriction, org_n):
        for i in restriction:
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

print(constraint_satisfactions( 6,[2,1,1]))



