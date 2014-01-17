__author__ = 'issahar'

import sys
import os
import os.path
import shutil
from datetime import datetime, time
import sqlite3
import hashlib
# print md5("string").hexdigest()

Verbose = False

global ignoreList
ignoreList = []
global index_path
index_path = ''
global last_db_file
last_db_file = ''

copiedFiles = 0
skippedFiles = 0
createdFolders = 0
deletedFolders = 0
deletedFiles = 0
errors = 0


def remove_dir(path):

    for root, dirs, files in os.walk(path, False):
        for f in files:
            os.unlink(os.path.join(root, f))

        for d in dirs:
            os.rmdir(os.path.join(root, d))

    os.rmdir(path)


def copy_file(from_filename, to_filename):

    is_copy = True
    if os.path.isfile(to_filename):
        from_stat = os.stat(from_filename)
        to_stat = os.stat(to_filename)

        is_copy = (from_stat.st_size != to_stat.st_size) or (str(from_stat.st_mtime) != str(to_stat.st_mtime))

    # Copy file with stat info, including e.g. modification date
    if is_copy:
        shutil.copy2(from_filename, to_filename)
        try:
            conn = sqlite3.connect(index_path)
            c = conn.cursor()
            sql = "CREATE TABLE IF NOT EXISTS 'Check' (path TEXT, hash TEXT)"
            c.execute(sql)
            path = from_filename
            fd = open(path, 'rb')
            b = fd.read()
            file_hash = hashlib.sha256(b).hexdigest()
            fd.close()

            #file_hash = md5(path).hexdigest()
            sql = "INSERT INTO 'Check' (path, hash) VALUES ('"+from_filename+"', '"+file_hash+"')"
            c.execute(sql)
            conn.commit()
            c.close()
        except:
           print "SQL error with file %s" % from_filename

    return is_copy


def create_folder_struc(path):

    return {'full_path': path,
            'files': [],
            'dirs': {}}


def make_dir_tree(path, data):

    try:
        for branch in os.listdir(path):
            new_path = os.path.join(path, branch)

            # Ignore some folders from proccessing
            if (branch.lower() in ignoreList) or (new_path.lower() in ignoreList):
                continue

            if os.path.isfile(new_path):
                data['files'].append(branch)
            elif os.path.isdir(new_path):
                data['dirs'][branch] = create_folder_struc(new_path)

                make_dir_tree(new_path, data['dirs'][branch])
    except:
        pass


def copy_folder(src_dirs, out_dirs, type=0):
    ''' type = 1 if full'''

    global copiedFiles
    global skippedFiles
    global createdFolders
    global deletedFolders
    global deletedFiles
    global errors

    for s in src_dirs['dirs']:
        if s not in out_dirs['dirs']:
            if s in out_dirs['files']:
                full_filename = os.path.join(out_dirs['full_path'], s)
                os.unlink(full_filename)
                if Verbose:
                    print('D %s' % full_filename)
                deletedFiles += 1

            out_dirs['dirs'][s] = create_folder_struc(os.path.join(out_dirs['full_path'], s))

            full_path = os.path.join(out_dirs['full_path'], s)
            os.mkdir(full_path)
            if Verbose:
                print('M [%s]' % full_path)
            createdFolders += 1
        if type == 1:
            copy_folder(src_dirs['dirs'][s], out_dirs['dirs'][s], 1)
        else:
            copy_folder(src_dirs['dirs'][s], out_dirs['dirs'][s])

    for o in out_dirs['dirs']:
        if o not in src_dirs['dirs']:
            full_path = os.path.join(out_dirs['dirs'][o]['full_path'])
            remove_dir(full_path)
            if Verbose:
                print('D [%s]' % full_path)
            deletedFolders += 1

    for o in out_dirs['files']:
        if o not in src_dirs['files']:
            full_filename = os.path.join(out_dirs['full_path'], o)
            os.unlink(full_filename)
            if Verbose:
                print('D %s' % full_filename)
            deletedFiles += 1

    for s in src_dirs['files']:
        full_from = os.path.join(src_dirs['full_path'], s)
        full_to = os.path.join(out_dirs['full_path'], s)

        if type == 1:
            copy_file(full_from, full_to)
            copiedFiles += 1
        else:
            if not SQL_check(last_db_file, full_from):
                copy_file(full_from, full_to)
                copiedFiles += 1
            else:
                skippedFiles += 1
                pass


def read_config(OutputFolder, full=False):
    RootFoldersFile = "tobackup.lst"
    IgnoreFoldersFile = "ignore.lst"
    ExtraFile = "extra.lst"

    if full:
        OutputFolder += '/full_' + datetime.now().strftime("%d.%b.%y_%H.%M")
    else:
        OutputFolder += '/' + datetime.now().strftime("%d.%b.%y_%H.%M")
    #print OutputFolder

    #read tobackup.lst
    if not os.path.isfile(RootFoldersFile):
        print("! %s doesn't exist" % RootFoldersFile)
        exit(1)
    #create folder for new one
    if not os.path.isdir(OutputFolder):
        try:
            os.makedirs(OutputFolder)
        except:
            print("! Can't create output folder %s" % OutputFolder)
            exit(1)

    #make list of folders
    rootFolders = [i.strip() for i in open(RootFoldersFile, "r").readlines()]
    if '' in rootFolders:
        rootFolders.remove('')

    #make ignore list
    global ignoreList
    if os.path.isfile(IgnoreFoldersFile):
        ignoreList = [line.strip().lower() for line in open(IgnoreFoldersFile, "r").readlines()]
        if '' in ignoreList:
            ignoreList.remove('')

    #make extra list
    extraList = ''
    if os.path.isfile(ExtraFile):
        extraList = [i.strip().lower() for i in open(ExtraFile, "r").readlines()]
        if '' in extraList:
            extraList.remove('')

        print('Extra files...')

    return rootFolders, extraList, OutputFolder


def SQL_check(last_db_file, check_file):
    try:
        conn = sqlite3.connect(last_db_file)
        c = conn.cursor()

        fd = open(check_file, 'rb')
        b = fd.read()
        file_hash = hashlib.sha256(b).hexdigest()
        fd.close()

        sql = "SELECT hash from 'Check' WHERE path='" + check_file + "'"
        c.execute(sql)
        tmp = c.fetchone()
        #c.close()

        if str(tmp[0]) == file_hash:
            c.close()
            return True
        else:
            print "was changed file %s, new hash: %s" % (check_file, str(tmp[0]))
            #hash was changed, update it
            sql = "UPDATE 'Check' SET hash='" + file_hash + "'" + "WHERE path='" + check_file + "'"
            c.execute(sql)
            conn.commit()
            c.close()
            return False
    except:
        print "SQL error with file %s" % check_file
        return False


def make_full(OutputFolder):
    rootFolders, extraList, OutputFolder = read_config(OutputFolder, True)
    #print rootFolders, ignoreList, extraList

    errors = 0
    for rootFolder in rootFolders:
        inputTree = create_folder_struc(rootFolder)
        make_dir_tree(rootFolder, inputTree)

        outFolder = inputTree['full_path']
        outFolder = outFolder.replace(':', '_')
        outFolder = os.path.join(OutputFolder, outFolder)

        print('[%s] -> [%s]...' % (rootFolder, outFolder))

        if not os.path.isdir(outFolder):
            try:
                os.makedirs(outFolder)
                print('Maked dir: [%s]' % outFolder)
            except:
                print("! Can't create output folder [%s]" % outFolder)
                print("! Skip input folder %s" % rootFolder)
                errors += 1
                continue

        global index_path
        index_path = OutputFolder+'\\findex.db'

        outputTree = create_folder_struc(outFolder)
        make_dir_tree(outFolder, outputTree)
        copy_folder(inputTree, outputTree, 1)

    print('Backing files...')

    for file_in_line in extraList:
        outFileDir = os.path.join(OutputFolder, os.path.dirname(file_in_line).replace(':', '_'))
        if not os.path.isdir(outFileDir):
            try:
                os.makedirs(outFileDir)
            except:
                print("! Can't create output folder [%s]. Skip extra file %s" % (outFileDir, file_in_line))
                errors += 1
                continue

        fullTo = os.path.join(outFileDir, os.path.basename(file_in_line))

        copy_file(file_in_line, fullTo)
        global copiedFiles
        copiedFiles += 1

    print "Errors: %s" % errors
    print "Copied: %s" % copiedFiles
    print('==============================')
    print("Done")


def make_differ(OutputFolder):
    rootFolders, extraList, OutputFolder = read_config(OutputFolder)
    errors = 0

    os.chdir(OutputFolder)
    os.chdir('../')
    dirs = os.listdir(os.getcwd())
    #make list of databases
    dbs = []
    for dir in dirs:
        if dir[:4] == 'full':
            os.chdir(OutputFolder+'/../'+dir)
            dbs.append(os.getcwd() + "/findex.db")
    print dbs
    #and choose the last
    global last_db_file
    last_db_file = dbs[0]
    for db in dbs[1:]:
        if os.stat(db).st_mtime < last_db_file:
            last_db_file = db
    print last_db_file

    #make copy to the same sir, as last backup
    OutputFolder = last_db_file[:-9]

    #elementary copy
    for rootFolder in rootFolders:
        inputTree = create_folder_struc(rootFolder)
        make_dir_tree(rootFolder, inputTree)

        outFolder = inputTree['full_path']
        outFolder = outFolder.replace(':', '_')
        outFolder = os.path.join(OutputFolder, outFolder)

        print('[%s] -> [%s]...' % (rootFolder, outFolder))

        if not os.path.isdir(outFolder):
            try:
                os.makedirs(outFolder)
                print('Maked dir: [%s]' % outFolder)
            except:
                print("! Can't create output folder [%s]" % outFolder)
                print("! Skip input folder %s" % rootFolder)
                errors += 1
                continue

        global index_path
        index_path = OutputFolder+'\\findex.db'

        outputTree = create_folder_struc(outFolder)
        make_dir_tree(outFolder, outputTree)
        copy_folder(inputTree, outputTree)

    print('Backing files...')

    for file_in_line in extraList:
        outFileDir = os.path.join(OutputFolder, os.path.dirname(file_in_line).replace(':', '_'))
        if not os.path.isdir(outFileDir):
            try:
                os.makedirs(outFileDir)
            except:
                print("! Can't create output folder [%s]. Skip extra file %s" % (outFileDir, file_in_line))
                errors += 1
                continue

        fullTo = os.path.join(outFileDir, os.path.basename(file_in_line))
        #there we make hash to look in bd
        if not SQL_check(last_db_file, file_in_line):
            copy_file(file_in_line, fullTo)
            global copiedFiles
            copiedFiles += 1
        else:
            global skippedFiles
            skippedFiles += 1
            pass
    print "Errors: %s, skipped: %s, copied: %s" % (errors, skippedFiles, copiedFiles)


def make_increment(OutputFolder):
    print "incr done"
    pass