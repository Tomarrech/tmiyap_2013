__author__ = 'issahar'
import sys
import time
import re
# 192.168.1.1-192.168.1.225,192.168.2.1 20-80,99 2
# 192.168.1.1,192.168.1.225,192.168.2.1 20-80,99 2
# 192.168.1.1-192.168.1.225,192.168.2.1-192.168.2.255,127.0.0.1 20-80,99 2
print 'first:', sys.argv[1]
print 'second:', sys.argv[2]
print 'third:', sys.argv[3]
ips = []
# r'[0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]'
input = sys.argv[1]
ranges = input.split(',')
reg = '([1-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])[- /.]([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])' \
      '[- /.]([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])[- /.]([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])'


def make_ip_list(start_ip, last_ip):
    #print start_ip, last_ip
    s1, s2, s3, s4 = start_ip.split('.')
    print 'start ',s1, s2, s3, s4
    l1, l2, l3, l4 = last_ip.split('.')
    print 'last', l1, l2, l3, l4
    host_list = []
    while True:
        if int(s1) == int(l1) and int(s2) == int(l2):
            if int(s3) == int(l3):
                if int(s4) != int(l4):
                    size = int(l4)-int(s4)
                    host_list.append(str(s1)+'.'+str(s2)+'.'+str(s3)+'.'+str(s4))
                    for i in range(size):
                        s4 = int(s4) + 1
                        host_list.append(str(s1)+'.'+str(s2)+'.'+str(s3)+'.'+str(s4))
                else:
                    break
            else:
                if int(s4) <= 254:
                    size = 255-int(s4)
                    host_list.append(str(s1)+'.'+str(s2)+'.'+str(s3)+'.'+str(s4))
                    for i in range(size):
                        s4 = int(s4) + 1
                        host_list.append(str(s1)+'.'+str(s2)+'.'+str(s3)+'.'+str(s4))
                    time.sleep(1)
                s3 = int(s3) + 1
                s4 = 1
        else:
            print "too long ip range, aborting..."
            return None
    print "Done!\n"
    return host_list

for ran in ranges:
    if not '-' in ran:
        if re.match(reg, ran):
            ips.append(ran)
    else:
        a, b = ran.split('-')
        if re.match(reg, a) and re.match(reg, b):
            ips.extend(make_ip_list(a, b))
        else:
            er_key = True
print len(ips)