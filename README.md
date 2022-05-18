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

## Advanced

There is a script called "kick" that can be called to bump a channel up to being run now.  You can either provide the channel by name or by path, or you can just go to the channel's folder and call it with no argument.

## To Do

Move the various configurations into an external configuration file so that reconfiguration is one-and-done.

Make all paths part of the configuration and get rid of hard-coded paths.

General clean-up

## Bugs


