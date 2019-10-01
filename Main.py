#----------------------------------------------------------------------------------------------------------------------
# BINARY CONVERSIONS + PRINTING
# convert string to list
def getListFromStr(string):
    list = [None]*len(string)
    counter = 0
    for i in string:
        list[counter] = i
        counter+=1
    return list

# convert list to string
def getStrFromList(list):
    return ''.join(list)

# print number - WORKS
def printNum(binaryList):
    print(getStrFromList(binaryList))

# make int numbers binary. Note: outputs a list.
def getBinList(integer):
    binaryString = '{0:08b}'.format(integer)
    binaryList = getListFromStr(binaryString)
    return binaryList

# make binary numbers int.
def getInt(binaryList):
    binaryString = getStrFromList(binaryList)
    return int(binaryString, 2)
#----------------------------------------------------------------------------------------------------------------------
# CALCULATOR OPERATIONS

# make binary numbers add
def add(numOne, numTwo):                                        #TODO: add stuff to make sure input is binary string
    numOneBin = getBinList(numOne)
    numTwoBin = getBinList(numTwo)
    result = ['0']*len(numOneBin)
    for digit in range(len(numOneBin)-1, -1, -1):               # range(start, end, step)
        if numOneBin[digit] == '0' and numTwoBin[digit] == '0':
            pass
        elif numOneBin[digit] == '1' and numTwoBin[digit] == '1':
            result = addOneToDigit(result, digit-1)
        else:                                                   # if one digit is 1 and the other is 0
            result = addOneToDigit(result, digit)
    return getInt(result)

# make binary numbers subtract
def subtract(numOne, numTwo):                                   # TODO: add stuff to make sure input is binary string + numOne>numTwo
    numOneBin = getBinList(numOne)                              # TODO: include negative numbersca
    numTwoBin = getBinList(numTwo)
    result = numOneBin
    for digit in range(len(numOneBin)-1, -1, -1):
        if numOneBin[digit] == numTwoBin[digit]:
            result[digit] = '0'
        elif numOneBin[digit] == '1' and numTwoBin[digit] == '0':
            result[digit] = '1'
        else:
            result = minusOneFromDigit(result, digit)
    return getInt(result)

def addOneToDigit(binaryList, digit):                           # for carry over (e.g. in base 10, 5+7=12)
    if binaryList[digit] == '0':
        binaryList[digit] = '1'
    else:
        binaryList[digit] = '0'
        addOneToDigit(binaryList, digit+1)
    return binaryList

def minusOneFromDigit(binaryList, digit):
    if binaryList[digit] == '1':
        binaryList[digit] = '0'
    else:
        binaryList[digit] = '1'
        minusOneFromDigit(binaryList, digit-1)
    return binaryList

# make int numbers multiply
def multiply(numOne, numTwo):                                   # TODO: add stuff to make sure these are each integers
    dummyVar = numOne
    for i in range(numTwo - 1):
        numOne = add(numOne, dummyVar)
    return numOne

# make int numbers divide
def divide(numOne, numTwo):                                   # TODO: atm divide can only do integers. Also need to make sure numOne>numTwo
    counter = 0
    while(numOne != 0):
        numOne = subtract(numOne, numTwo)
        counter += 1
    return counter

# make int numbers raise to power


# route of int numbers?


