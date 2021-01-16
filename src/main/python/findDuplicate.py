import sys
import os
import hashlib

check_path = (lambda filepath, hashes, p = sys.stdout.write:
        (lambda hash = hashlib.sha1 (file (filepath).read ()).hexdigest ():
                ((hash in hashes) and (p ('DUPLICATE FILE\n'
                                          '   %s\n'
                                          'of %s\n' % (filepath, hashes[hash])))
                 or hashes.setdefault (hash, filepath)))())

scan = (lambda dirpath, hashes = {}: 
                map (lambda (root, dirs, files):
                        map (lambda filename: check_path (os.path.join (root, filename), hashes), files), os.walk (dirpath)))