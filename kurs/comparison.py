#!/usr/bin/env python
# -*- coding: utf_8 -*-
__author__ = 'issahar'
import sqlite3
import os


def comparison_port(open_ports):
    try:
        if not os.path.exists('./ports.db'):
            raise NameError('FileNotFoundError ')
        conn = sqlite3.connect("./ports.db")
        c = conn.cursor()

        for host in open_ports:
            print "\nFor host %s were associated next ports:" % host

            for port in open_ports[host]:
                t = (port,)
                c.execute('select * from ports where port=?', t)
                tmp = c.fetchone()
                if tmp:
                    print "\t%d\t\t-> %s" % (port, tmp[1].encode('1251'))
                else:
                    print "\t%d\t\t-> is unknown" % port
        c.close()
    except NameError:
        print "Sorry, but our data-base file is absent today..."
        for host in open_ports:
            print "\nFor host %s were founded next ports:" % host
            print open_ports[host]