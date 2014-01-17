__author__ = 'issahar'

import sys
import os
import os.path
import shutil
from hashlib import md5
# print md5("string").hexdigest()

Verbose = False

ignoreList = []

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


def copy_folder(src_dirs, out_dirs):

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

        been_copied = copy_file(full_from, full_to)
        if been_copied:
            flag = 'C'
            copiedFiles += 1
        else:
            flag = '-'
            skippedFiles += 1

        if Verbose and been_copied:
            print('%s %s -> %s' % (flag, full_from, full_to))


def make_full():
    print "full done"
    pass


def make_differ():
    print "differ done"
    pass


def make_increment():
    print "incr done"
    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: backup.py <output folder> [--verbose]")
        print('E.g.: "backup.py C:\Users\tomar_000\Dropbox\Backup\"')
        exit(1)

    RootFoldersFile = "tobackup.lst"
    IgnoreFoldersFile = "ignore.lst"
    ExtraFile = "extra.lst"
    OutputFolder = sys.argv[1]

    try:
        back_type = (sys.argv[2] == '--verbose')
    except:
        pass

    if not os.path.isfile(RootFoldersFile):
        print("! %s doesn't exist" % RootFoldersFile)
        exit(1)

    if not os.path.isdir(OutputFolder):
        try:
            os.makedirs(OutputFolder)
        except:
            print("! Can't create output folder %s" % OutputFolder)
            exit(1)

    rootFolders = [i.strip() for i in open(RootFoldersFile, "r").readlines()]
    if '' in rootFolders:
        rootFolders.remove('')

    if os.path.isfile(IgnoreFoldersFile):
        ignoreList = [i.strip().lower() for i in open(IgnoreFoldersFile, "r").readlines()]
        if '' in ignoreList:
            ignoreList.remove('')

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
                print('M [%s]' % outFolder)
            except:
                print("! Can't create output folder [%s]" % outFolder)
                print("! Skip input folder %s" % rootFolder)
                errors += 1
                continue

        outputTree = create_folder_struc(outFolder)
        make_dir_tree(outFolder, outputTree)

        copy_folder(inputTree, outputTree)

    if os.path.isfile(ExtraFile):
        extraList = [i.strip().lower() for i in open(ExtraFile, "r").readlines()]
        if '' in extraList:
            extraList.remove('')

        print('Extra files...')

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

            copied = copy_file(file_in_line, fullTo)
            if copied:
                c = 'C'
                copiedFiles += 1
            else:
                c = '-'
                skippedFiles += 1

            if Verbose and copied:
                print('%s %s -> %s' % (c, file_in_line, fullTo))

    print('==============================')
    print('Copied file(s):    %d' % copiedFiles)
    print('Skipped file(s):   %d' % skippedFiles)
    print('Created folder(s): %d' % createdFolders)
    print('Deleted folder(s): %d' % deletedFolders)
    print('Deleted file(s):   %d' % deletedFiles)
    print('Errors:            %d' % errors)
    print('==============================')
    print("Done")