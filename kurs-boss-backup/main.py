__author__ = 'tomar_000'
#coding: utf-8
import sys
from timetable import make_timetable
from backup import *

if __name__ == "__main__":

    if len(sys.argv) == 1:
        #was used by user
        OutputFolder = raw_input("Please, type OutputFolder for making backups"
                                 "\[Ex: home/user/Dropbox/Backup]\n$>")
        #remember path for backups

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
        do_now = False
        if raw_input("Done full backup of directory? [no - if not]\n$>") == "no":
            print("ok, all types of back will be done by timetable. Bye!")
        else:
            print("ok, making full backup now...")
            if not OutputFolder:
                OutputFolder = open("./destination", 'r').read()
            make_full(OutputFolder)

    elif len(sys.argv) == 2:
        #was used by cron
        try:
            OutputFolder = open("./destination", 'r').read()
            if not OutputFolder:
                print "Destination file is empty, aborting..."
                exit(403)

            if not os.path.isdir(OutputFolder):
                try:
                    os.makedirs(OutputFolder)
                except:
                    print("! Can't create output folder %s" % OutputFolder)
                    exit(403)

            backup_type = sys.argv[1]
            if backup_type[2:] in ['full', 'differ', 'increment']:
                print "Now making %s backup to %s..." % (backup_type[2:], OutputFolder)
                if backup_type[2:] == 'full':
                    make_full(OutputFolder)
                elif backup_type[2:] == 'differ':
                    make_differ(OutputFolder)
                else:
                    make_increment(OutputFolder)
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