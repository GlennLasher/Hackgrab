#!/usr/bin/python

import os

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

    def destroy(self):
        #TODO: This.
        pass
