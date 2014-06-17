__author__ = 'tomar_000'
#coding: utf-8
#var = 7

IP = [8, 7, 3, 2, 5, 4, 1, 6]

E_p = [7, 3, 6, 2, 5, 4, 1, 8, 7, 6, 3, 1]

S_1 = [1, 5, 1, 4, 2, 6, 6, 3, 4, 5, 5, 7, 2, 2, 3, 7]

S_2 = [4, 5, 2, 5, 7, 6, 1, 3, 1, 2, 7, 4, 7, 3, 3, 6]

S_3 = [[3, 1, 2, 1],
       [3, 2, 2, 1],
       [2, 3, 1, 3],
       [1, 3, 2, 1]]

Table = [[0, 1, 4, 3],  # Vh S1 S2 S3
         [1, 5, 5, 1],
         [2, 1, 2, 2],
         [3, 4, 5, 1],
         [4, 2, 7, 3],
         [5, 6, 6, 2],
         [6, 6, 1, 2],
         [7, 3, 3, 1],
         [8, 4, 1, 2],
         [9, 5, 2, 3],
         [10, 5, 7, 1],
         [11, 7, 4, 3],
         [12, 2, 7, 1],
         [13, 2, 3, 3],
         [14, 3, 3, 2],
         [15, 7, 6, 1]]

#A = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


def make_table(d_A, S_table):

    d_C = {}
    for i, a in enumerate(S_table):
        v_1 = a
        _d_A = i ^ d_A
        v_2 = S_table[_d_A]
        _d_C = v_1 ^ v_2
        #print bin(i), '\t', bin(v_1), '\t', bin(_d_A), '\t', bin(v_2), '\t', bin(_d_C)
        if bin(_d_C) in d_C:
            d_C[bin(_d_C)] += 1
        else:
            d_C[bin(_d_C)] = int(1)
    res = {}
    res['C'] = {}
    for v, col in d_C.items():
        if col == max(d_C.values()):
            res['C'][v] = col
            #print v, col, '\n----------------------'
    res['A'] = bin(d_A)[2:].zfill(4)
    rez = [res]
    #print rez
    return rez


def get_max_for_block(S):
    res_d_C = []
    maximum = 0
    for A in range(1, 16):
        for var in make_table(A, S):
            #print var
            #будем хранить значения для пересечений. первое сравнение по А, второе по С

            if var['A'] not in res_d_C:
                for C in var['C'].keys():
                    #print var['C'][C]
                    if var['C'][C] > maximum:  # тут мы и найдем наш максимум
                        maximum = var['C'][C]
                        res_d_C = [var]
                    elif var['C'][C] == maximum:
                        maximum = var['C'][C]
                        res_d_C.append(var)
    #print res_d_C

    for elem in res_d_C:
        print 'значение бит dA:', elem['A'], 'dC:', elem['C'].keys()[0][2:].zfill(3), 'частота: ', elem['C'].values()[0]
    print "-------------------------"


def out(a, S):
        st = int(a[0::3], 2)
        row = int(a[1:-1], 2)
        return S[st][row]

new_S3 = [out(el, S_3) for el in [bin(i)[2:].zfill(4) for i in xrange(16)]]

print "для Блока 1:\n", get_max_for_block(S_1)
print "для Блока 2:\n", get_max_for_block(S_2)
print "для Блока 3:\n", get_max_for_block(new_S3)