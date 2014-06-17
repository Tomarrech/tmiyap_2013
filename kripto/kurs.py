__author__ = 'tomarech@gmail.com'
#coding: utf-8
import tables

key = '0010110100110001001100110011000100101110001001110010010000100010'
message = '010010001111101101000000111010101110010111000010110100010010010101100000101001001001001101111011' \
          '000110001010110100111110001011110100110110110100001100010100010101010111110111111000001001110010'
decodedMessage = ''


def make_56BitKey(key):
    result = ''

    for i in range(56):
        result += key[tables.tableFor56Key[i]-1]
    return result


def makeLeftShift(num, key):
    return key[-num:] + key[:-num]


def makeSubKey(key):
    result = ''

    for i in range(48):
        result += key[tables.tableForCompressionTo48[i]-1]
    return result

Key56bit = make_56BitKey(key)

lKey = makeLeftShift(-1, Key56bit[:28])
rKey = makeLeftShift(-1, Key56bit[28:])

keyAfterFirstShift = lKey + rKey
firstSubKey = makeSubKey(keyAfterFirstShift)
print '1st SubKey: ', firstSubKey

l2Key = makeLeftShift(-1, lKey)
r2Key = makeLeftShift(-1, rKey)

keyAfterSecondShift = l2Key + r2Key
secondSubKey = makeSubKey(keyAfterSecondShift)
print '2nd SubKey: ', secondSubKey

l3Key = makeLeftShift(-2, l2Key)
r3Key = makeLeftShift(-2, r2Key)

keyAfterThirdShift = l3Key + r3Key
thirdSubKey = makeSubKey(keyAfterThirdShift)
print '3rd SubKey: ', thirdSubKey
print "==============================================================\n\n"


def iterationXlXr(mess, round=1):

    def makeIPShift(mes):
        result = ''
        XL = ''
        for i in range(64):
            result += mes[tables.tableIP[i]-1]
            if i == 31:
                XL = result
                result = ''
        return XL, result

    if round == 1:
        XL, XR1 = makeIPShift(mess)  #shiftIP do only first round
    else:
        XL = mess[:32]
        XR1 = mess[32:]

    def makeShiftExt(xr):
        result = ''
        for i in range(48):
            result += xr[tables.shftWithExtension[i]-1]
        return result

    XR = makeShiftExt(XR1)

    if round == 1:
        xorXR = int(XR, 2) ^ int(thirdSubKey, 2)  # 3,2,1 подключи оответственно
    elif round == 2:
        xorXR = int(XR, 2) ^ int(secondSubKey, 2)
    else:
        xorXR = int(XR, 2) ^ int(firstSubKey, 2)
    xstr = str(bin(xorXR))[2:].zfill(48)

    def shiftSblocksAndP(mes):
        mesAfterS = ''
        result = ''
        for i in range(1, 9):
            S = mes[(i-1)*6:i*6]
            line = S[0]+S[5]
            column = S[1:5]
            mesAfterS += bin(tables.S[i-1][int(line, 2)][int(column, 2)])[2:].zfill(4)
        for i in range(32):
            result += mesAfterS[tables.shiftP[i]-1]
        return result

    XRAfterFFunction = shiftSblocksAndP(xstr)

    xorXL = int(XL, 2) ^ int(XRAfterFFunction, 2)
    xorXL = bin(xorXL)[2:].zfill(32)

    if round == 3:
        return xorXL+XR1
    return XR1+xorXL


def makeThreeRounds(mess):

    def makeReverseIPShift(mes):
        result = ''
        XL = ''
        for i in range(64):
            result += mes[tables.tebleReverseIP[i]-1]
            if i == 31:
                XL = result
                result = ''
        return XL+result

    firstRound = iterationXlXr(mess)  # 1.2.3 part

    secondRound = iterationXlXr(firstRound, 2)

    thirdRound = iterationXlXr(secondRound, 3)

    revers = makeReverseIPShift(thirdRound)
    return revers

first64Byte = message[:64]
decodedMessage += makeThreeRounds(first64Byte)

second64Byte = message[64:128]
decodedMessage += makeThreeRounds(second64Byte)

third64Byte = message[128:]
decodedMessage += makeThreeRounds(third64Byte)

print "decrypted message in hex:"
for i in range(1, 25):
    letter = decodedMessage[(i-1)*8:i*8]
    letterHex = hex(int(letter, 2))[2:]
    print letterHex,