__author__ = 'issahar'
import sys
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
    print start_ip, last_ip


for ran in ranges:
    if not '-' in ran:
        if re.match(reg, ran):
            ips.append(ran)
    else:
        a, b = ran.split('-')
        if re.match(reg, a) and re.match(reg, b):
            make_ip_list(a, b)
        else:
            er_key = True
print ips

#if re.split(r'\S', str(sys.argv[1])):
#    print 'range'
#else:
#    print "list"
#for ip in ipv4_re:
#    print ip