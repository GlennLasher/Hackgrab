#!/usr/bin/python3

import os
import time
import re

relevantre = re.compile ("^(.*)\.mp4$")

for filename in os.listdir():
    relevantmatch = relevantre.match(filename)
    if relevantmatch:
        stub    = relevantmatch.group(1)
        stats   = os.lstat(filename)
        date    = time.gmtime(stats.st_mtime)
        dateyr  = "%04d" % (date.tm_year,)
        datemn  = "%02d" % (date.tm_mon,)
        datedt  = "%02d" % (date.tm_mday,)

        target  = os.path.join(dateyr, datemn, datedt)
        desc    = "%s.description" % (relevantmatch.group(1),)
        moveto  = os.path.join(target, filename)

        print ("For", filename, ":")
        print ("    We will create", target)
        print ("    And move the file to", moveto)

                           
        os.makedirs(target, exist_ok = True)
        os.rename(filename, moveto)

        if os.path.isfile(desc):
            moveto  = os.path.join(target, desc)

            print ("    And move", desc)
            print ("    To", moveto)

            os.rename(desc, moveto)
            
        print ("")
