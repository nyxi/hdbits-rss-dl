#!/usr/bin/python

import urllib.request
import os
import re

def main():
    # Some variables
    RSSURL = 'https://hdbits.org/rss.php'
    PASSKEY = 'your-passkey' #Set this
    TORRENTDIR = '/home/emil/rtorrent/torrents/' #Change this
    SCRIPTDIR = '/home/emil/hdbits-rss/' #Change this to the directory where the script is
    TARGETS = SCRIPTDIR + 'targets' #Path to your file with search patterns

    # Checks the highest ID from last time we
    # ran the script so we only download NEW
    # torrents
    LASTID = '0'
    if os.path.isfile(SCRIPTDIR + 'hdbits-rss-filtered'):
        RSSFILE = open(SCRIPTDIR + 'hdbits-rss-filtered', 'r')
        LASTID = ''.join(re.split(' .*\n',RSSFILE.readline()))
        RSSFILE.close()
    
    # This messy section downloads the RSS file, filters it
    # and check if any of the torrents match any of the
    # search patterns in TARGETS, if there are any matches
    # the script downloads the torrent to TORRENTDIR
    urllib.request.urlretrieve(RSSURL + '?passkey=' + PASSKEY, SCRIPTDIR + 'hdbits-rss')
    # Open the RSS files
    RSSFILE = open(SCRIPTDIR + 'hdbits-rss', 'r')
    FRSS = open(SCRIPTDIR + 'hdbits-rss-filtered', 'w')
    # Loop the RSS file
    for line in RSSFILE:
        # Look for lines with 'guid' in them
        if 'guid' in line:
            # Remove HTML-tags and split the current line into a list
            FLIST = re.split('<.*?>',line)
            torrent = FLIST[4].replace(' ', '_') + '.torrent'
            # If we have a LASTID, begin looping
            # the TARGETS file looking for matches to download
            if (LASTID != '0'):
                TARGETFILE = open(TARGETS, 'r')
                for linex in TARGETFILE:
                    # Try all patterns from TARGETFILE against the current
                    # line from the RSS file
                    results = re.findall(linex.replace('\n', ''), FLIST[4])
                    # Check if we have a match and if it's a new torrent
                    if (results and int(FLIST[2]) > int(LASTID)):
                        # Download the torrent
                        urllib.request.urlretrieve('https://hdbits.org/download.php/' + torrent + '?id=' + FLIST[2] + '&passkey=' + PASSKEY + '&source=details', TORRENTDIR + torrent)
                TARGETFILE.close()
            # Write filtered lines to hdbits-rss-filtered
            FRSS.write(FLIST[2] + ' ' + FLIST[4] + '\n')
    RSSFILE.close()
    FRSS.close()

if __name__ == '__main__':
    main()
