#!/usr/bin/python3

import os
import re
import hashlib

hashfilename = "sha256sums"
hashfilere   = re.compile('^([0-9a-f]{64})  (.*)$')
filematchre  = re.compile('^.*\.(mp4|webm|mkv)')

#Function to hash a file
def hashfile(filepath):
    blocksize = 1048576
    
    if ((not os.path.exists(filepath)) or (not os.path.isfile(filepath))):
        return None
    
    digest = hashlib.sha256()
    with open(filepath, "rb") as fh:
        block = fh.read(blocksize)
        while (len(block) > 0):
            digest.update(block)
            block = fh.read(blocksize)
    return digest.hexdigest()


#Create empty dicts for the hashes
indict  = dict()
outdict = dict()

#If there is an existing sha256sums file, read it.
if os.path.isfile(hashfilename):
    with open(hashfilename, "r") as infile :
        for inline in infile:
            match = hashfilere.match(inline)
            if match:
                indict[match.group(2).strip()] = match.group(1)

#Walk the filesystem.  If the file is a relevant type and the path is in indict, copy it to outdict.
for dir in os.walk("."):
    current = os.path.relpath(dir[0])
    for thisfile in dir[2]:
        if filematchre.match(thisfile):
            filepath = os.path.join(current, thisfile)
            if filepath in indict:
                action = "REP"
                outdict[filepath] = indict[filepath]
            else:
                action = "GEN"
                outdict[filepath] = hashfile(filepath)
            print ("%s %s  %s" % (action, outdict[filepath], filepath), flush=True)

#Spit out the results
with open(hashfilename, 'w') as outfile:
    outfile.write("".join(["%s  %s\n" % (outdict[i], i) for i in sorted(outdict)]))
    
        
