__author__ = 'tomar_000'
#coding: utf-8
import sys
from timetable import make_timetable
from backup import *

if __name__ == "__main__":

    if len(sys.argv) == 1:
        #was used by user
        OutputFolder = raw_input("Please, type OutputFolder for making backups[C:\Users\tomar_000\Dropbox\Backup]\n$>")
        #remember path for backups
        RootFoldersFile = "tobackup.lst"
        IgnoreFoldersFile = "ignore.lst"
        ExtraFile = "extra.lst"

        if OutputFolder:
            f = open("./OutputFolder", 'w')
            f.write(OutputFolder)
            f.close()

        make_timetable()
        while True:
            if raw_input("Add new timetable? [no - if not]\n$>") == "no":
                break
            else:
                make_timetable()

    elif len(sys.argv) == 2:
        #was used by cron
        try:
            OutputFolder = open("./destination", 'r').read()
            if not OutputFolder:
                print "Destination file is empty, aborting..."
                exit(403)

            backup_type = sys.argv[1]
            if backup_type[2:] in ['full', 'differ', 'increment']:
                print "Now making %s backup to %s..." % (backup_type[2:], OutputFolder)
                if backup_type[2:] == 'full':
                    make_full()
                elif backup_type[2:] == 'differ':
                    make_differ()
                else:
                    make_increment()
            else:
                print "Uncorrected type."
        except:
            print "Destination file doesn't exist, aborting..."
            exit(404)
        print "Task done, bye!"
        exit(1)
    else:
        print("Usage: backup.py <type of backup if need> [--full/differ/increment]")
        exit(1)