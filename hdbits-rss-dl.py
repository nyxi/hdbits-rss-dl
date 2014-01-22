#!/usr/bin/python
# Add your hdbits passkey to PASSKEY variable
# Set path to where you want to save the .torrent files
# in the TORRENTDIR variable, don't forget trailing slash
# Edit the 'targets' file with the torrents you want to
# look for

import urllib2
import re

# Some variables
PASSKEY = 'passkey-goes-here' #Set this
TORRENTDIR = '/home/emil/rtorrent/torrents/' #Change this

#Read the search string file into a list
try:
    with open('targets', 'r') as f:
        TARGETS = []
        for line in f:
            TARGETS.append(line)
except:
    print "Error when trying to read 'targets' file, aborting"
    exit()

# Checks the highest ID from last time we
# ran the script so we only download NEW
# torrents
try:
    f = open('lastguid', 'r')
    LASTID = int(f.read().rstrip())
except:
    LASTID = 0

# Download the RSS file
r = urllib2.urlopen('http://hdbits.org/rss.php?passkey=%s' % (PASSKEY))
# Loop the RSS file
NEWGUID = None
for rssline in r:
    if 'guid' in rssline:
        # Remove HTML-tags and split the current line into a list
        FLIST = re.split('<.*?>',rssline)
        # FLIST[2] is the GUID and FLIST[4] contains the torrent title
        if FLIST[2] == '':
            continue
        if NEWGUID is None:
            NEWGUID = int(FLIST[2])
        for target in TARGETS:
            results = re.findall(target.rstrip().lower(), FLIST[4].lower())
            # Check if we have a match and if it's a new torrent
            if (results and int(FLIST[2]) > int(LASTID)):
                urltodl = 'https://hdbits.org/download.php/%s.torrent?id=%s&passkey=%s' % (FLIST[4].replace(' ', '%20'), FLIST[2], PASSKEY)
                # Download the .torrent file
                r = urllib2.urlopen(urltodl)
                with open('%s%s.torrent' % (TORRENTDIR, FLIST[4].replace(' ', '_')), 'wb') as torrent:
                    torrent.write(r.read())

# Update the 'lastguid' file
if NEWGUID is not None:
    with open('lastguid', 'w') as f:
        f.write(str(NEWGUID))
