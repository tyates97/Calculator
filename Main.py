# ----------------------------------------------------------------------------------------------------------------------
# BINARY CONVERSIONS, PRINTING,


# convert string to list
def get_list_from_str(string):
    return [digit for digit in string]


# convert list to string
def get_str_from_list(lis):
    return ''.join(lis)


# make int numbers binary. note: outputs a list.
def get_bin_list(integer):
    binary_string = '{0:08b}'.format(integer)
    binary_list = get_list_from_str(binary_string)
    return binary_list


# make binary numbers int.
def get_int(binary_list):
    binary_string = get_str_from_list(binary_list)
    return int(binary_string, 2)


# check if number is negative
def is_negative(binary_list):
    if binary_list[0] is '-':
        return True
    else:
        return False


# makes two numbers the same length
def modify_len(modified_list, target_list):
        while len(modified_list) < len(target_list):        #TODO: find way to get rid of operator here
            modified_list = ['0'] + modified_list
        return modified_list


# if the binary numbers are zero up to the specified digit
def rest_are_zeros(lis, digit):
    for i in range(digit):
        if lis[i] is '1':
            return False
    return True

def make_positive(num):
    num_bin = get_bin_list(num)
    if num_bin[0] is '-':
        num_bin[0] = '0'
        return get_int(num_bin)
    else:
        return num


def make_negative(num):
    num_bin = get_bin_list(num)
    if num_bin[0] is '-':
        return num
    else:
        num_bin = ['-'] + num_bin
        return get_int(num_bin)


# TODO: make a make_positive_bin(binary_list) function, then change all list[0] = '0' to make_positive_bin(list). Easier to read + reduces repeated code
# TODO: same thing with make_negative and list = ['-'] + list
# ----------------------------------------------------------------------------------------------------------------------
# OPERATIONS: BOOLEAN LOGIC
# TODO: make sure is efficient

# checks if one binary number is greater than the other
def is_greater_than(big_bin_num, small_bin_num):
    # NB to use modify_len here, you have to use < in modify_len
    big_bin_num = modify_len(big_bin_num, small_bin_num)
    small_bin_num = modify_len(small_bin_num, big_bin_num)
    # if both numbers positive
    if not is_negative(big_bin_num) and not is_negative(small_bin_num):
        for digit in range(len(big_bin_num)):
            if big_bin_num[digit] is '1' and small_bin_num[digit] is '0':     # if there's a 1 in bin_num_one before bin_num_two
                return True
            elif big_bin_num[digit] is '0' and small_bin_num[digit] is '1':   # if there's a 1 in bin_num_two before bin_num_one
                return False
            # special case: when the 2 numbers are identical
            elif len(big_bin_num) is 1 and len(small_bin_num) is 1 and big_bin_num[0] is small_bin_num[0]:
                return False
            else:
                pass
    # if 1st number positive & 2nd negative
    elif not is_negative(big_bin_num) and is_negative(small_bin_num):
        return True
    # if 1st number negative & 2nd positive
    elif is_negative(big_bin_num) and not is_negative(small_bin_num):
        return False
    # if 1st and 2nd numbers negative, opposite of their positive counterparts
    else:
        big_bin_num[0] = '0'
        small_bin_num[0] = '0'
        result = not is_greater_than(big_bin_num, small_bin_num)
        big_bin_num[0] = '-'
        small_bin_num[0] = '-'
        return result


# ----------------------------------------------------------------------------------------------------------------------
# OPERATIONS: ADDITION
# TODO: make sure is efficient

# make binary numbers add
def add(num_one, num_two):                                                  # TODO: add user sanitation
    num_one = get_bin_list(num_one)                                         # make numbers binary
    num_two = get_bin_list(num_two)
    num_one = modify_len(num_one, num_two)                                  # making binary numbers same size (adding 0s)
    num_two = modify_len(num_two, num_one)
    result = ['0']*len(num_one)                                             # initialise result (easier than appending)

    '''
    With subtraction there are 4 possible cases: num_one/num_two is neg/pos.
    The below determines which of the possible four cases we have.
    Example cases are commented next to their according if statement, for clarity.
    '''

    if not is_negative(num_one) and not is_negative(num_two):               # case: add(100, 2)
        # this is the case where the addition actually happens
        for digit in range(len(num_one)-1, -1, -1):
            if num_one[digit] is '0' and num_two[digit] is '0':
                pass
            elif num_one[digit] is '1' and num_two[digit] is '1':
                result = add_one_to_digit(result, digit-1)
            else:       # if one digit is 1 and the other is 0
                result = add_one_to_digit(result, digit)
        return get_int(result)

    elif is_negative(num_one) and not is_negative(num_two[0]):              # case: add(-100, 2)
        del num_one[0]                      # could change first element, but this accounts for larger lists.
        num_one = modify_len(num_one, num_two)
        return subtract(get_int(num_two), get_int(num_one))

    elif is_negative(num_two) and not is_negative(num_one):                 # case: add(100, -2)
        del num_two[0]
        num_two = modify_len(num_two, num_one)
        return subtract(get_int(num_one), get_int(num_two))

    else:                                                                   # case: add(-100, -2)
        num_one[0] = '0'
        num_two[0] = '0'
        return get_int(['-'] + get_bin_list(add(get_int(num_one), get_int(num_two))))


# deals with the carry
def add_one_to_digit(binary_list, digit):                           # for carry over (e.g. in base 10, 5+7=12)
    if digit is -1:
        return ['1'] + binary_list
    elif  digit is 0 and binary_list[0] is '1':
        binary_list[0] = '0'
        return ['1'] + binary_list
    else:
        if binary_list[digit] is '0':
            binary_list[digit] = '1'
        else:
            binary_list[digit] = '0'
            add_one_to_digit(binary_list, digit-1)
        return binary_list


# ----------------------------------------------------------------------------------------------------------------------
# OPERATIONS: SUBTRACTION - NOTE YOU ARE SUBTRACTING ARG2 FROM ARG1
# TODO: make sure is efficient

# make binary numbers subtract.
def subtract(num_one, num_two):                                     # TODO: add user sanitation
    num_one = get_bin_list(num_one)                                 # TODO: include negative numbers
    num_two = get_bin_list(num_two)
    num_one = modify_len(num_one, num_two)
    num_two = modify_len(num_two, num_one)

    '''
    With subtraction there are 8 possible cases: num_one is larger, num_two is larger and num_one/num_two is neg/pos.
    This is because subtracting a big number from a small number is different from vice versa
    The below determines which of the possible eight cases we have.
    Example cases are commented next to their according if statement, for clarity.
    '''

    if is_greater_than(num_one, num_two):
        if not is_negative(num_one) and not is_negative(num_two):       # case: subtract(100,2)
            ''' *** NB this case is where the subtraction actually happens. The rest is recursive/uses add(). *** '''
            result = num_one[:]                                         # result is the bigger number
            for digit in range(len(num_one) - 1, -1, -1):
                if num_one[digit] is num_two[digit]:
                    result[digit] = '0'
                elif num_one[digit] is '1' and num_two[digit] is '0':
                    result[digit] = '1'
                else:
                    result = minus_one_from_digit(result, digit)
                    num_one[digit - 1] = '0'
            return get_int(result)

        elif not is_negative(num_one) and is_negative(num_two):         # case: subtract(100, -2) & subtract(2, -100)
            num_two[0] = '0'
            return add(get_int(num_one), get_int(num_two))
        else:                                                           # case: subtract(-2, -100)
            num_two[0] = '0'
            return add(get_int(num_one), get_int(num_two))

    elif is_greater_than(num_two, num_one):
        if not is_negative(num_one) and not is_negative(num_two):       # case: subtract(2,100)
            result_pos = subtract(get_int(num_two), get_int(num_one))
            result_bin = get_bin_list(result_pos)
            result = ['-'] + result_bin
            return get_int(result)
        elif is_negative(num_one) and not is_negative(num_two):         # case: subtract(-2, 100), subtract(-100, 2)
            num_two = ['-'] + num_two
            return add(get_int(num_one), get_int(num_two))
        else:                                                           # case: subtract(-100, -2)
            num_two[0] = '0'
            return add(get_int(num_one), get_int(num_two))                                # TODO: repeating code from l172-174. can you condense?
    else:                                                               # case: subtract(8,8), subtract(-8,-8)
        return 0


# deals with the carry
def minus_one_from_digit(binary_list, digit):
    if binary_list[digit] is '1':
        binary_list[digit] = '0'
        # checks if rest of digits are zeros - will be true if subtracting a larger number from a smaller.
    elif rest_are_zeros(binary_list, digit):
        binary_list = ['-'] + binary_list
    else:
        binary_list[digit] = '1'
        minus_one_from_digit(binary_list, digit-1)
    return binary_list

# ----------------------------------------------------------------------------------------------------------------------


# make int numbers multiply
def multiply(num_one, num_two):                                     # TODO: add user sanitation & check if can simplify
    if is_negative(get_bin_list(num_one)) and not is_negative(get_bin_list(num_two)):          # case: multiply(-100, 2)
        return make_negative(multiply(make_positive(num_one), num_two))
    elif not is_negative(get_bin_list(num_one)) and is_negative(get_bin_list(num_two)):        # case: multiply(100, -2)
        return make_negative(multiply(num_one, make_positive(num_two)))
    elif is_negative(get_bin_list(num_one)) and is_negative(get_bin_list(num_two)):            # case: multiply(-100, -2)
        return multiply(make_positive(num_one), make_positive(num_two))
    else:                                                                                      # case: multiply(100, 2)
        dummy_var = num_one
        for i in range(num_two - 1):
            num_one = add(num_one, dummy_var)
        return num_one


# make int numbers divide
def divide(num_one, num_two):                                       # TODO: atm divide can only do positive integers. Also need to make sure num_one>num_two
    counter = 0
    while num_one is not 0:
        num_one = subtract(num_one, num_two)
        counter = add(counter, 1)
    return counter

# make int numbers raise to power


# route of int numbers?

#TODO: real bug testing. All edge cases. numbers above 255, negatives/positives, big/small for all operations


