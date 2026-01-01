#!/usr/bin/python3

import os
import time
import re
import json

relevantre = re.compile ("^(.*\\])\\.(mp4|webm|mkv|mp3|m4a)$")
new_filename = 'new.m3u'

new_content = []
new_update  = False

if os.path.isfile(new_filename):
    with open(new_filename, 'r') as infile:
        new_content = infile.read().strip().split('\n')

for filename in os.listdir():
    relevantmatch = relevantre.match(filename)
    if relevantmatch:
        stub    = relevantmatch.group(1)
        desc    = "%s.description" % (stub,)
        info    = "%s.info.json" % (stub,)

        if os.path.isfile(info):
            with open(info, 'r') as infile:
                jsdata = json.load(infile)
            ytdate  = jsdata['upload_date']
            dateyr  = ytdate[0:4]
            datemn  = ytdate[4:6]
            datedt  = ytdate[6:8]
        else:
            stats   = os.lstat(filename)
            date    = time.gmtime(stats.st_mtime)
            dateyr  = "%04d" % (date.tm_year,)
            datemn  = "%02d" % (date.tm_mon,)
            datedt  = "%02d" % (date.tm_mday,)

        target  = os.path.join(dateyr, datemn, datedt)
        moveto  = os.path.join(target, filename)

        print ("For", filename, ":")
        print ("    We will create", target)
        print ("    And move the file to", moveto)

        new_content.append(moveto)
        new_update = True
                           
        os.makedirs(target, exist_ok = True)
        os.rename(filename, moveto)

        if os.path.isfile(desc):
            moveto  = os.path.join(target, desc)

            print ("    And move", desc)
            print ("    To", moveto)

            os.rename(desc, moveto)

        if os.path.isfile(info):
            moveto  = os.path.join(target, info)

            print ("    And move", info)
            print ("    To", moveto)

            os.rename(info, moveto)

        print ("", flush=True)

if new_update:
    with open(new_filename, "w") as outfile:
        outfile.write("\n".join(new_content[-10:]) + '\n')
