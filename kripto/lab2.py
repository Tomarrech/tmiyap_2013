def ToBinary(x):
    n = "" if x > 0 else "0"
    while x > 0:
        y = str(x % 2)
        n = y + n
        x = int(x / 2)
    if len(n) == 1:
        n = '000' + str(n)
    elif len(n) == 2:
        n = '00' + str(n)
    elif len(n) == 3:
        n = '0' + str(n)
    return(n)

def ToBin(x):
    n = "" if x > 0 else "0"
    while x > 0:
        y = str(x % 2)
        n = y + n
        x = int(x / 2)
    if len(n) == 1:
        n = '00' + str(n)
    elif len(n) == 2:
        n = '0' + str(n)
    return(n)

def ToB(x):
    n = "" if x > 0 else "0"
    while x > 0:
        y = str(x % 2)
        n = y + n
        x = int(x / 2)
    if len(n) == 1:
        n = '0' + str(n)
    return(n)

def ToDec(x):
    amount_sign = len(x)
    trans_num = 0
    for n in x:
        s = int(n) * int(2) ** (amount_sign - 1)
        trans_num += s
        amount_sign -= 1
    return trans_num
#TabS1 = [1, 5, 1, 4, 2, 6, 6, 3, 4, 5, 5, 7, 2, 2, 3, 7]
#TabS2 = [4, 5, 2, 5, 7, 6, 1, 3, 1, 2, 7, 4, 7, 3, 3, 6]
#TabS3 = [3, 1, 2, 1,  3, 2, 2, 1,  2, 3, 1, 3,  1, 3, 2, 1]

S1 = ['0000#001', '0001#101', '0010#001', '0011#100', '0100#010', '0101#110', '0110#110', '0111#011','1000#100', '1001#101', '1010#101', '1011#111', '1100#010', '1101#010',  '1110#011', '1111#111']

S2 = ['0000#100', '0001#101', '0010#010', '0011#101', '0100#111', '0101#110', '0110#001', '0111#011', '1000#001', '1001#010', '1010#111', '1011#100', '1100#111', '1101#011', '1110#011', '1111#110']

S3 = ['0000#11', '0010#01', '0100#10', '0110#01',
      '0001#11', '0011#10', '0101#10', '0111#01',
      '1000#10', '1010#11', '1100#01', '1110#11',
      '1001#01', '1011#11', '1101#10', '1111#01']

""" For S1 and S2 blocks"""
temp = []
temp1 = []
for I in range(1, 16):
    i = ToBinary(I)
    for J in range(1, 8):
        count = 0
        j = ToBin(J)
        for el in S2:
            temp = []
            temp1 = []

            entry = el[0:4]
            output = el[5:]

            if i[0] == '1':
                temp.append(entry[0])
            if i[1] == '1':
                temp.append(entry[1])
            if i[2] == '1':
                temp.append(entry[2])
            if i[3] == '1':
                temp.append(entry[3])

            if j[0] == '1':
                temp1.append(output[0])
            if j[1] == '1':
                temp1.append(output[1])
            if j[2] == '1':
                temp1.append(output[2])


            if len(temp) == 1:
                res1 = int(temp[0])
            if len(temp) == 2:
                res1 = int(temp[0]) ^ int(temp[1])
            if len(temp) == 3:
                res1 = int(temp[0]) ^ int(temp[1]) ^ int(temp[2])
            if len(temp) == 4:
                res1 = int(temp[0]) ^ int(temp[1]) ^ int(temp[2]) ^ int(temp[3])


            if len(temp1) == 1:
                res2 = int(temp1[0])
            if len(temp1) == 2:
                res2 = int(temp1[0]) ^ int(temp1[1])
            if len(temp1) == 3:
                res2 = int(temp1[0]) ^ int(temp1[1]) ^ int(temp1[2])

            if res1 == res2:
                count += 1
        print i, j, count

print " For S3 block"

temp = []
temp1 = []
for I in range(1, 16):
    i = ToBinary(I)
    for J in range(1, 4):
        count = 0
        j = ToB(J)
        for el in S3:

            temp = []
            temp1 = []

            entry = el[0:4]
            output = el[5:]

            if i[0] == '1':
                temp.append(entry[0])
            if i[1] == '1':
                temp.append(entry[1])
            if i[2] == '1':
                temp.append(entry[2])
            if i[3] == '1':
                temp.append(entry[3])

            if j[0] == '1':
                temp1.append(output[0])
            if j[1] == '1':
                temp1.append(output[1])

            if len(temp) == 1:
                res1 = int(temp[0])
            if len(temp) == 2:
                res1 = int(temp[0]) ^ int(temp[1])
            if len(temp) == 3:
                res1 = int(temp[0]) ^ int(temp[1]) ^ int(temp[2])
            if len(temp) == 4:
                res1 = int(temp[0]) ^ int(temp[1]) ^ int(temp[2]) ^ int(temp[3])


            if len(temp1) == 1:
                res2 = int(temp1[0])
            if len(temp1) == 2:
                res2 = int(temp1[0]) ^ int(temp1[1])
            if res1 == res2:
                count += 1
        print i, j, count
