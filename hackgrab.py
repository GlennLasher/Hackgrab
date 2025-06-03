#!/usr/bin/python

import os
import time
import re

class Loggable (object):
    def __init__(self, debug=False, verbose=False):
        self.debug    = debug
        self.verbose  = debug or verbose

    def message(self, message_text, debug):
        if self.verbose or (self.debug and debut):
            print(message_text)

class Channel (Loggable):
    def __init__ (self, url = None, name = None, basepath =
                  "/srv/hackgrab", lowpri = False, debug = False,
                  verbose = False):

        super().__init__(debug, verbose)
        
        self.url         = url
        self.name        = name
        self.basepath    = basepath
        self.lowpri      = lowpri
        self.channelpath = os.path.join(self.basepath, "content", self.name)

    def create(self, overwrite = False, destroy = False):
        if self.exists():
            if destroy:
                self.destroy()
            elif not overwrite:
                raise Exception ("Channel.create():  Channel %s already exists." % (self.name, ))

            
        os.makedirs(self.channelpath)
        with open (os.path.join(self.channelpath, "url"), "w") as outfile:
            outfile.write(self.url + "\n")
        with open (os.path.join(self.channelpath, "validated"), "w") as outfile:
            outfile.write("NEW\n")
        with open (os.path.join(self.channelpath, "archive"), "w") as outfile:
            pass
        with open (os.path.join(self.channelpath, "sha256sums"), "w") as outfile:
            pass
        if self.lowpri:
            with open (os.path.join(self.channelpath, ".lowpri"), "w") as outfile:
                pass
        
    def exists(self, complete=False):
        good=os.path.exists(self.channelpath) and os.path.isdir(self.channelpath)

        if good and complete:
            for element in ["archive", "sha256sums", "url", "validated"]:
                elpath = os.path.join(self.channelpath, element)
                good = good and os.path.exists(elpath) and os.path.isfile(elpath)

        return good

    def datesort(self):
        relevantre = re.compile ("^(.*\])\.(mp4|webm|mkv)$")
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
                stats   = os.lstat(filename)
                date    = time.gmtime(stats.st_mtime)
                dateyr  = "%04d" % (date.tm_year,)
                datemn  = "%02d" % (date.tm_mon,)
                datedt  = "%02d" % (date.tm_mday,)

                target  = os.path.join(dateyr, datemn, datedt)
                desc    = "%s.description" % (relevantmatch.group(1),)
                moveto  = os.path.join(target, filename)

                if self.verbose:
                    print ("For", filename, ":")
                    print ("    We will create", target)
                    print ("    And move the file to", moveto)

                new_content.append(moveto)
                new_update = True
        
                os.makedirs(target, exist_ok = True)
                os.rename(filename, moveto)

                if os.path.isfile(desc):
                    moveto  = os.path.join(target, desc)

                    if self.verbose:
                        print ("    And move", desc)
                        print ("    To", moveto)
                        print ("", flush=True)

                    os.rename(desc, moveto)
            
        if new_update:
            with open(new_filename, "w") as outfile:
                outfile.write("\n".join(new_content[-10:]) + '\n')
    
    def destroy(self):
        #TODO: This.
        pass
