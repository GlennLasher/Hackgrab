# Hackgrab

Collection of scripts to manage low-impact bulk downloads from YouTube

## Why?

Some years ago, there was a concern that some YouTube channels that are of interest to me might get removed from YouTube.  My automatic response was to start downloading them en masse.

This quickly became unwieldy.

My next step was to create a script that contained all of the commands that I ran regularly to keep everything updated.  It wasn't a well-structured script, it just consisted of one line for each of the channels I wanted to capture, calling youtube-dl and sha256sums against them.  Later, this was changed to use yt-dlp.

This quickly becamse unmaintainable.

That brings us to here.  Contained in this repository are a set of scripts that are easily configured to grab full YouTube channels and keep the content organized.

## Prerequisites

You will need a Linux system with Python 3.x, Bash (already on Linux by default), mediainfo, sha256sum and cron.

In python3, you will need the modules hashlib, os, re and time, which I believe are all installed by default.

## Setup

By default, the scripts are written to use /srv/hackgrab as the home folder.

Under /srv/hackgrab, create the following folders: bin, content, dothese, logs, metadata.

Copy all of the scripts from this repository into bin.

In the content folder, create a directory to contain a channel you want to capture.  In that folder, create a file called url that contains the URL of the channel.  Create a file called validated that contains just the word "NEW".

For instance, to start fetching Technology Connections, you would:

 * create a folder at /srv/hackgrab/content/Technology Connections
 * create a file in that folder called url that contains "https://www.youtube.com/c/TechnologyConnections/videos"
 * create a file in that folder called validated that contains the word "NEW"

Finally, to set it in motion, create two cron jobs:

    #Hackgrab
    #Min  Hour             Day Month Weekday Command
     00   *                *   *     *       /srv/hackgrab/bin/grab_one >> /srv/hackgrab/logs/log 2>&1
     15   */3              *   *     *       /srv/hackgrab/bin/validate_one >> /srv/hackgrab/logs/log 2>&1

You can, obviously, change the timings on that to your liking, but what it does is:

 * Once per hour, find the channel least recently update, and update it
 * Every third hour, find the one least recently validated and validate it.

## Script explanations

### aggressive_loop

This takes no arguments.  It will loop over all of the currently-active channels and call launch on each individually, grabbing all of the channels in one go.  This is for bringing all of the channels up to date in a hurry.

### datesort.py

This takes no arguments.  It will read the timestamp on all files with extensions mp4, webm or mkv, create a folder of the format YYYY/MM/DD if there isn't one already, and moves the file and its accompanying description there.  Once it's done this, it will add it to a list of new files.  The list of new files will be trimmed to the ten newest entries and saved as new.m3u.

### grab_one

This is the heart of hackgrab.

It will start by checking to see if there is already an instance running on this node, and bail out if it is.  It will also check to see if this channel is being run on another node.  It will return exit code 2 if there is another instance here, or 3 if this channel is running elsewhere.

If it has been provided with an argument, it will use that as a channel name; otherwise, it will look for the channel whose url file has the least recent timestamp and that will be the channel it works with at this point.

If there is a flag set by aggressive_loop, it will remove it (this is key to aggressive_loop knowing when it's finished running).

It will update the timestamp on the url file to now.  This will push this channel to the end of the queue.

It will set a lock on the channel so that other nodes don't start to run it.

It will look for any files in a folder called 'dothis' and execute them before proceeding.

It will call yt-dlp to download the channel.

It will update the timestamps on all of the media files, and call datesort.py.

It will call update_hash.py

It will remove the lock.

It will check to see if there is any content in the last 90 days (you can alter this limit) and if not, it will make the channel inactive by renaming the url file to url_hold.  It will also do this if there is a file here named .lowpri.

### kick

This can take a channel name as an argument, or it can be called from a channel folder.  It will change the timestamp on url for the specified channel to 1970-01-01 (putting it at the top of the queue, since that's over fifty years ago) and then call launch.

### reactivate

This takes no arguments.  It will loop over all of the channels and rename url_hold to url, reactivating any inactive channels.  The idea is to call this about once a month so that low-priority and low-activity channels get scanned infrequently.

### show_status

This takes no arguments, and produces a status screen for the cluster, filesystem and queue.

### update_hash.py

This takes no arguments.  It will read any existing file named sha256sums, remove any entries for files that are not present, and compute values for any files that are not on the list before rewriting it.

### validate_one

This will find the channel whose sha256 hashes were least frequently run.  It uses the timestamp on the file "validated" to decide which one to run, and will write a one-word result to that file.  

## Advanced

This can be run on a cluster by having a set of worker nodes all mount the folder from a NAS.  The requirements for each worker node are the same as running it on a single node:  Python 3, mediainfor, ffmpeg (optional), yt-dlp.  The list of these can be included in the SERVERLIST variable in launch.  Launch will select a node at random to run it on.  The primary purpose of this is to allow for the IP address presented to YouTube to vary.  This is, ideally, done using IPv6.  Inter-node communication is via SSH, so you will need to establish key-based login.

Any desktop or laptop that might mount the network share can also run the launch or kick script, or any of the others, really, allowing you to make things happen without needing to log in directly to the cluster. 

## To Do

Move the various configurations into an external configuration file so that reconfiguration is one-and-done.

Make all paths part of the configuration and get rid of hard-coded paths.

## Bugs


