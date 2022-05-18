#!/usr/bin/python3

import os
import re

renamere = re.compile("^(.*)\-(...........)\.mp4$")

for inname in os.listdir():
    match = renamere.match(inname)
    if match:
        (title, ytid) = (match.group(1), match.group(2))
        outname = "%s [%s].mp4" % (title, ytid)
        print ("From:")
        print ("  %s" % (inname,))
        print ("To:")
        print ("  %s" % (outname,))
        print ("")
        os.rename (inname, outname)
    else:
        print ("Skipping:")
        print ("  %s" % (inname,))
        print ("")
