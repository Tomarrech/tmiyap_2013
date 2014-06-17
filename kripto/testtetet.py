Alfa = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
Betta = [1, 2, 3, 4, 5, 6, 7]
Betta3 = [1, 2, 3]
Vh = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

TabS1 = [1, 5, 1, 4, 2, 6, 6, 3, 4, 5, 5, 7, 2, 2, 3, 7]
TabS2 = [4, 5, 2, 5, 7, 6, 1, 3, 1, 2, 7, 4, 7, 3, 3, 6]
TabS3 = [3, 1, 2, 1, 3, 2, 2, 1, 2, 3, 1, 3, 1, 3, 2, 1]


def make_tabs(tab_number):
    f = open("resulttab" + str(tab_number) + ".txt", "a")
    f.write('Alfa Betta Count' + '\n')
    for i in range(0, len(Alfa)):
        for l in range(0, len(Betta)):
            countt = res1 = res2 = 0
            for j in range(0, len(Vh)):
                if str(tab_number) == '1':
                    Vi = (TabS1[Vh[j]])
                elif str(tab_number) == '2':
                    Vi = (TabS2[Vh[j]])
                else:
                    break
                temp1 = Vh[j] & Alfa[i]
                temp2 = Vi & Betta[l]
                for k in range(2, len(bin(temp1))):
                    res1 = res1 ^ int(bin(temp1)[k])
                for k in range(2, len(bin(temp2))):
                    res2 = res2 ^ int(bin(temp2)[k])
                if res1 == res2:
                    countt = countt + 1
                res1 = 0
                res2 = 0
            print (str(bin(Alfa[i])) + '\t' + str(bin(Betta[l])) + '\t' + str(countt) + '\n')
            if countt <= 4 or countt >= 12:
                f.write(str(bin(Alfa[i])) + '\t' + str(bin(Betta[l])) + '\t' + str(countt) + '\n')
    f.close()


def make_tab3():
    f = open("resulttab3.txt", "a")
    f.write('Alfa Betta Count' + '\n')
    for i in range(0, len(Alfa)):
        for l in range(0, len(Betta3)):
            countt = res1 = res2 = 0
            for j in range(0, len(Vh)):
                Vi = (TabS3[Vh[j]])
                temp1 = Vh[j] & Alfa[i]
                temp2 = Vi & Betta[l]
                for k in range(2, len(bin(temp1))):
                    res1 = res1 ^ int(bin(temp1)[k])
                for k in range(2, len(bin(temp2))):
                    res2 = res2 ^ int(bin(temp2)[k])
                if res1 == res2:
                    countt = countt + 1
                res1 = res2= 0
            print (str(bin(Alfa[i])) + '\t' + str(bin(Betta[l])) + '\t' + str(countt) + '\n')
            if countt <= 4 or countt >= 12:
                f.write(str(bin(Alfa[i])) + '\t' + str(bin(Betta[l])) + '\t' + str(countt) + '\n')
    f.close()
make_tabs(1)
make_tabs(2)
make_tab3()
