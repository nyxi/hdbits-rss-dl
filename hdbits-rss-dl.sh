#!/bin/sh

RSSURL="https://hdbits.org/rss.php"
PASSKEY="your-passkey" # Add your passkey here
TORRENTDIR="/home/emil/rtorrent/torrents/" # Directory to save the torrents in
SCRIPTDIR="/home/emil/hdbits-rss/" # Path to the directory where this script is located

cd $SCRIPTDIR

# Check the highest id from last time we scraped
# the RSS so we only look for new torrents since then
if [ -f hdbits-rss-filtered ]; then
	LASTID="$(head -n1 hdbits-rss-filtered | sed 's/ .*//g')"
fi
# Get the RSS file
curl -o hdbits-rss $RSSURL?passkey=$PASSKEY

# Filters the RSS file so every line will be:
# id title
grep "guid" hdbits-rss | sed 's/^.*false">//g; s/<\/guid><title>/ /g; s/<\/title>//g' > hdbits-rss-filtered
rm hdbits-rss

# The matching and download section,
# only runs if we have a $LASTID
# Should only miss $LASTID the very first
# time the script is run
if [ "$LASTID" != "" ]; then
	# Grep for matches in hdbits-rss-filtered
	# and read every line
	while read LINE; do
		ID="$(echo $LINE | sed 's/ .*//')"
		TITLE="$(echo $LINE | cut -d \  -f 2- | sed 's/ /_/g')"
		# If a match has a id greater than $LASTID it is
		# a new torrent and we want to download it
		if [ "$ID" -gt "$LASTID" ]; then
			curl -o "$TITLE.torrent" "https://hdbits.org/download.php/$TITLE.torrent?id=$ID&passkey=$PASSKEY&source=details"
			mv *.torrent $TORRENTDIR
		fi
	done <<< "$(grep -f targets hdbits-rss-filtered)"
fi
