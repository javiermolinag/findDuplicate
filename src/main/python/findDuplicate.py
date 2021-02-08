# dupFinder.py - https://www.pythoncentral.io/finding-duplicate-files-with-python/
import os, sys
import hashlib
 
def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName, flush=True)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups
 
 
# Joins two dictionaries
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]
 
 
def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
 
 
def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('Duplicates Found:', flush=True)
        print('The following files are identical. The name could differ, but the content is identical', flush=True)
        print('___________________', flush=True)
        for result in results:
            for subresult in result:
                print('\t\t%s' % subresult)
            print('___________________', flush=True)
 
    else:
        print('No duplicate files found.', flush=True)
 
 
if __name__ == '__main__':
    sys.stdout = open('../../../log/output.stdout', 'w')
    if len(sys.argv) > 1:
        dups = {}
        folders = sys.argv[1:]
        for i in folders:
            print("Check for folder", i, flush=True)
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                joinDicts(dups, findDup(i))
            else:
                print('%s is not a valid path, please verify' % i, flush=True)
                sys.exit()
        printResults(dups)
    else:
        print('Usage: python dupFinder.py folder OR \n python dupFinder.py folder1 folder2 folder3', flush=True)