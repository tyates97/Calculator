# BINARY CONVERSIONS, PRINTING,


# convert string to list
def get_list_from_str(string):
    return [digit for digit in string]


# convert list to string
def get_str_from_list(lis):
    return ''.join(lis)


# make int numbers binary. note: outputs a list.
def get_bin_list(integer):
    return get_list_from_str('{0:08b}'.format(integer))


# make binary numbers int.
def get_int(binary_list):
    return int(get_str_from_list(binary_list), 2)


# check if number is negative
def is_negative(binary_list):
    return True if binary_list[0] is '-' else False


# makes two numbers the same length
def modify_len(modified_list, target_list):
    while len(modified_list) < len(target_list):        #TODO: find way to get rid of operator here
        if not is_negative(modified_list):
            modified_list = ['0'] + modified_list
        else:
            modified_list = ['-'] + make_pos_bin(modified_list)
    return modified_list


# if the binary numbers are zero up to the specified digit
def rest_are_zeros(lis, digit):
    for i in range(digit):
        if lis[i] is '1':
            return False
    return True


def make_pos_num(num):
    return None if num is None else get_int(make_pos_bin(get_bin_list(num)))


def make_neg_num(num):
    return None if num is None else get_int(make_neg_bin(get_bin_list(num)))


def make_pos_bin(binary_list):
    if binary_list[0] is '-':
        binary_list[0] = '0'
    return binary_list


def make_neg_bin(binary_list):
    if binary_list[0] is not '-':
        binary_list = ['-'] + binary_list
    return binary_list


# ---------------------------------------------------------------------------------------------------------------------


# checks if one binary number is greater than the other
def is_greater_than(big_bin_num, small_bin_num):
    # NB to use modify_len here, you have to use < in modify_len
    big_bin_num = modify_len(big_bin_num, small_bin_num)
    small_bin_num = modify_len(small_bin_num, big_bin_num)
    if not is_negative(big_bin_num) and not is_negative(small_bin_num):
        for digit in range(len(big_bin_num)):
            if big_bin_num[digit] is '1' and small_bin_num[digit] is '0':     # if there's a 1 in bin_num_one before bin_num_two
                return True
            elif big_bin_num[digit] is '0' and small_bin_num[digit] is '1':   # if there's a 1 in bin_num_two before bin_num_one
                return False
            # special case: when the 2 numbers are identical
            elif len(big_bin_num) is 1 and len(small_bin_num) is 1 and big_bin_num[0] is small_bin_num[0]:
                return False
    elif not is_negative(big_bin_num) and is_negative(small_bin_num):
        return True
    elif is_negative(big_bin_num) and not is_negative(small_bin_num):
        return False
    else:
        return not is_greater_than(make_pos_bin(big_bin_num), make_pos_bin(small_bin_num))


# ---------------------------------------------------------------------------------------------------------------------
# TODO: add user sanitation

# make binary numbers add
def add(num_one, num_two):
    num_one = modify_len(get_bin_list(num_one), get_bin_list(num_two))
    num_two = modify_len(get_bin_list(num_two), num_one)
    result = ['0']*len(num_one)                                             # initialise result (easier than appending)

    if is_negative(num_one) and not is_negative(num_two):                   # case: add(-100, 2)
        return subtract(get_int(num_two), get_int(make_pos_bin(num_one)))
    elif is_negative(num_two) and not is_negative(num_one):                 # case: add(100, -2)
        return subtract(get_int(make_pos_bin(num_one)), get_int(num_two))
    elif is_negative(num_one) and is_negative(num_two):                     # case: add(-100, -2). Horrible line, but computationally cheapest method
        return get_int(make_neg_bin(get_bin_list(add(get_int(make_pos_bin(num_one)), get_int(make_pos_bin(num_two))))))
    else:                                                                   # case: add(100, 2)
        ''' *** NB this case is where the addition actually happens. The rest is recursive/uses subtract(). *** '''
        for digit in range(len(num_one) - 1, -1, -1):
            if num_one[digit] is '0' and num_two[digit] is '0':
                pass
            elif num_one[digit] is '1' and num_two[digit] is '1':
                result = add_one_to_digit(result, digit - 1)
            else:  # if one digit is 1 and the other is 0
                result = add_one_to_digit(result, digit)
        return get_int(result)


# deals with the carry
def add_one_to_digit(binary_list, digit):
    if digit is -1:
        return ['1'] + binary_list
    elif digit is 0 and binary_list[0] is '1':
        binary_list[0] = '0'
        return ['1'] + binary_list
    elif binary_list[digit] is '0':
        binary_list[digit] = '1'
        return binary_list
    else:
        binary_list[digit] = '0'
        add_one_to_digit(binary_list, digit-1)
        return binary_list


# ----------------------------------------------------------------------------------------------------------------------
# TODO: add user sanitation

# make binary numbers subtract.
def subtract(num_one, num_two):
    num_one = modify_len(get_bin_list(num_one), get_bin_list(num_two))
    num_two = modify_len(get_bin_list(num_two), num_one)

    if is_negative(num_two):
        return add(get_int(num_one), get_int(make_pos_bin(num_two)))
    elif is_negative(num_one) and not is_negative(num_two):
        return add(get_int(num_one), get_int(make_neg_bin(num_two)))
    elif not is_negative(num_one) and not is_negative(num_two) and is_greater_than(num_two, num_one):
        return make_neg_num(subtract(get_int(num_two), get_int(num_one)))
    else:                                                           # subtracting a small +ve num from a large +ve num
        ''' *** NB this case is where the subtraction actually happens. The rest is recursive/uses add(). *** '''
        for digit in range(len(num_one) - 1, -1, -1):
            if num_one[digit] is num_two[digit]:
                num_one[digit] = '0'
            elif num_one[digit] is '1' and num_two[digit] is '0':
                num_one[digit] = '1'
            else:
                num_one = minus_one_from_digit(num_one, digit)
        return get_int(num_one)


# deals with the carry
def minus_one_from_digit(binary_list, digit):
    if binary_list[digit] is '1':
        binary_list[digit] = '0'
        # checks if rest of digits are zeros - will be true if subtracting a larger number from a smaller.
    elif rest_are_zeros(binary_list, digit):
        binary_list = make_neg_bin(binary_list)
    else:
        binary_list[digit] = '1'
        minus_one_from_digit(binary_list, digit-1)
    return binary_list

# ----------------------------------------------------------------------------------------------------------------------


# make int numbers multiply
def multiply(num_one, num_two):                                     # TODO: add user sanitation & check if can simplify
    if is_negative(get_bin_list(num_one)) and not is_negative(get_bin_list(num_two)):          # case: multiply(-100, 2)
        return make_neg_num(multiply(make_pos_num(num_one), num_two))
    elif not is_negative(get_bin_list(num_one)) and is_negative(get_bin_list(num_two)):        # case: multiply(100, -2)
        return make_neg_num(multiply(num_one, make_pos_num(num_two)))
    elif is_negative(get_bin_list(num_one)) and is_negative(get_bin_list(num_two)):            # case: multiply(-100, -2)
        return multiply(make_pos_num(num_one), make_pos_num(num_two))
    else:                                                                                      # case: multiply(100, 2)
        dummy_var = num_one
        for i in range(num_two - 1):
            num_one = add(num_one, dummy_var)
        return num_one


# make int numbers divide
def divide(num_one, num_two):                                                               # TODO: atm divide can only do positive integers.
    if not is_negative(get_bin_list(num_one)) and not is_negative(get_bin_list(num_two)):   # case: divide(100, 2)
        if is_greater_than(get_bin_list(num_two), get_bin_list(num_one)):
            print('This function can only return values that are integers. Dividing these arguments gives a decimal.')
            return None
        else:
            counter = 0
            while num_one is not 0:
                num_one = subtract(num_one, num_two)
                counter = add(counter, 1)
            return counter
    elif not is_negative(get_bin_list(num_one)) and is_negative(get_bin_list(num_two)):     # case: divide(100, -2)
        return make_neg_num(divide(num_one, make_pos_num(num_two)))
    elif is_negative(get_bin_list(num_one)) and not is_negative(get_bin_list(num_two)):     # case: divide(-100, 2)
        return make_neg_num(divide(make_pos_num(num_one), num_two))
    else:                                                                                   # case: divide(-100, -2)
        return divide(make_pos_num(num_one), make_pos_num(num_two))


# make int numbers raise to power


# route of int numbers?

