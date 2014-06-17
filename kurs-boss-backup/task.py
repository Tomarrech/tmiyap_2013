import sys
import os
import os.path
import tarfile
import time
import gzip
import copy
import shutil
 
Verbose = False
 
ignoreList = []
 
copiedFiles = 0
skippedFiles = 0
createdFolders = 0
deletedFolders = 0
deletedFiles = 0
errors = 0
 
def removeDir(path):
    '''
    Remove dir and all subdirs with all subfiles
    '''
    for root, dirs, files in os.walk(path, False):
        for f in files:
            os.unlink(os.path.join(root, f))
           
        for d in dirs:
            os.rmdir(os.path.join(root, d))
           
    os.rmdir(path)
   
def copyFile(fromFilename, toFilename):
    '''
    Function will copy file only if toFilename is different than fromFilename.
    Size and modification date checked.
   
    Returns True if file been realy copied,
    return False if there was no real copy (files seems the same)
    '''
    copy = True
    if os.path.isfile(toFilename):
        fromStat = os.stat(fromFilename)
        toStat = os.stat(toFilename)
 
        copy = (fromStat.st_size != toStat.st_size) or (str(fromStat.st_mtime) != str(toStat.st_mtime))       
 
    # Copy file with stat info, including e.g. modification date
    if copy:
        shutil.copy2(fromFilename, toFilename)
       
    return copy
 
def createFolderStruct(path):
    '''
    Create struct (tree node) for folder tree
    '''
    return {'full_path': path,
            'files': [],
            'dirs': {}}
 
def makeDirTree(path, data):
    '''
    Creates folder tree in form of special struct
    '''
    for i in os.listdir(path):
        newPath = os.path.join(path, i)
 
        # Ignore some folders from proccessing
        if (i.lower() in ignoreList) or (newPath.lower() in ignoreList):
            continue
       
        if os.path.isfile(newPath):
            data['files'].append(i)
        elif os.path.isdir(newPath):
            data['dirs'][i] = createFolderStruct(newPath)
           
            makeDirTree(newPath, data['dirs'][i])
           
def copyFolder(srcDirs, outDirs):
    '''
    Copy folder from "left" to "right", given folders trees srcDirs and outDirs.
    Right folder will be complete copy of left folder with minimum number of file operations
    (don't copy file if it's already exists and hasn't been modified)
    '''
   
    # Use global counters
    global copiedFiles
    global skippedFiles
    global createdFolders
    global deletedFolders
    global deletedFiles
    global errors   
   
    # Loop throught all src folders, s - current folder name
    for s in srcDirs['dirs']:
        # If src folder isn't exist in output folder
        if s not in outDirs['dirs']:
            # If there is file in output folder with name as folder in src folder - delete that file
            if s in outDirs['files']:
                # Delete file s
                fullFilename = os.path.join(outDirs['full_path'], s)
                os.unlink(fullFilename)
                if Verbose:
                    print('D %s' % fullFilename)
                deletedFiles += 1                                       
               
            outDirs['dirs'][s] = createFolderStruct(os.path.join(outDirs['full_path'], s))
           
            # Create output folder with src folder name               
            fullPath = os.path.join(outDirs['full_path'], s)
            os.mkdir(fullPath)
            if Verbose:
                print('M [%s]' % fullPath)
            createdFolders += 1
 
        # Go deep inside current folder
        copyFolder(srcDirs['dirs'][s], outDirs['dirs'][s])
   
    # Remove folders from right, that don't exist on left
    for o in outDirs['dirs']:
        if o not in srcDirs['dirs']:
            fullPath = os.path.join(outDirs['dirs'][o]['full_path'])
            removeDir(fullPath)
            if Verbose:
                print('D [%s]' % fullPath)
            deletedFolders += 1               
 
    # Remove files from right, that don't exist on left
    for o in outDirs['files']:
        if o not in srcDirs['files']:
            fullFilename = os.path.join(outDirs['full_path'], o)
            os.unlink(fullFilename)
            if Verbose:
                print('D %s' % fullFilename)
            deletedFiles += 1           
 
    # Copy files from left to right
    for s in srcDirs['files']:
        fullFrom = os.path.join(srcDirs['full_path'], s)
        fullTo = os.path.join(outDirs['full_path'], s)
       
        copied = copyFile(fullFrom, fullTo)
        if copied:
            c = 'C'
            copiedFiles += 1
        else:
            c = '-'
            skippedFiles += 1
           
        if Verbose and copied:
            print('%s %s -> %s' % (c, fullFrom, fullTo))
 
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: backup.py <output folder> [--verbose]")
        print('E.g.: "backup.py d:\\dropbox\\my dropbox\\backup\\"')
        exit(1)
 
    RootFoldersFile = "tobackup.lst"
    IgnoreFoldersFile = "ignore.lst"
    ExtraFile = "extra.lst"
    OutputFolder = sys.argv[1]
   
    try:
        Verbose = (sys.argv[2] == '--verbose')
    except:
        pass
 
    # Only mandatory file is RootFoldersFile, check that it exists
    if (not os.path.isfile(RootFoldersFile)):
        print("! %s doesn't exist" % RootFoldersFile)
        exit(1)
 
    # Output folder should exist, or we should be able to create it
    if not os.path.isdir(OutputFolder):
        try:
            os.makedirs(OutputFolder)
        except:
            print("! Can't create output folder %s" % OutputFolder)
            exit(1)
 
    # Read root folders from file, skip empty lines
    rootFolders = [i.strip() for i in open(RootFoldersFile, "r").readlines()]
    if '' in rootFolders:
        rootFolders.remove('')
 
    # Read list of folders that need to be ignored (if specified)
    if (os.path.isfile(IgnoreFoldersFile)):
        ignoreList = [i.strip().lower() for i in open(IgnoreFoldersFile, "r").readlines()]
        if '' in ignoreList:
            ignoreList.remove('')
 
    # Create folders trees for each input folder
    for rootFolder in rootFolders:
        inputTree = createFolderStruct(rootFolder)
        makeDirTree(rootFolder, inputTree)
 
        # File will be placed under OutputFolder plus full path to src folder
        # E.g. src folder d:\projects\python will be copied to folder q:\backup\d_\projects\python
        #                 ^^^^^^^^^^^^^^^^^^                                    ^^^^^^^^^^^^^^^^^^           
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
       
        # Make folder tree for real output folder
        outputTree = createFolderStruct(outFolder)       
        makeDirTree(outFolder, outputTree)
       
        # Copy input folder to output folder
        copyFolder(inputTree, outputTree)
       
    # Read list of extra files
    if (os.path.isfile(ExtraFile)):
        extraList = [i.strip().lower() for i in open(ExtraFile, "r").readlines()]
        if '' in extraList:
            extraList.remove('')
       
        print('Extra files...')
       
        for file in extraList:
            outFileDir = os.path.join(OutputFolder, os.path.dirname(file).replace(':', '_'))
            if not os.path.isdir(outFileDir):
                try:
                    os.makedirs(outFileDir)
                except:
                    print("! Can't create output folder [%s]. Skip extra file %s" % (outFileDir, file))
                    errors += 1
                    continue
       
            fullTo = os.path.join(outFileDir, os.path.basename(file))
       
            copied = copyFile(file, fullTo)
            if copied:
                c = 'C'
                copiedFiles += 1
            else:
                c = '-'
                skippedFiles += 1
               
            if Verbose and copied:
                print('%s %s -> %s' % (c, file, fullTo))
           
    print('==============================')
    print('Copied file(s):    %d' % copiedFiles)
    print('Skipped file(s):   %d' % skippedFiles)
    print('Created folder(s): %d' % createdFolders)
    print('Deleted folder(s): %d' % deletedFolders)
    print('Deleted file(s):   %d' % deletedFiles)
    print('Errors:            %d' % errors)
    print('==============================')   
    print("Done")