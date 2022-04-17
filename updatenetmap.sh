#!/bin/bash


# Todo - Use http://www.cidr-report.org/as2.0/autnums.html to make names out of this and then use 'tag' to get the name?

echo "Starting prefix update"

cd /tmp
# Clean old data
rm -f oix-full-snapshot-latest.dat.bz2
rm -f oix-full-snapshot-latest.dat

wget http://archive.routeviews.org/oix-route-views/oix-full-snapshot-latest.dat.bz2
echo "Routeviews downloaded"

bzip2 -d oix-full-snapshot-latest.dat.bz2 
echo "Routeviews unpacked"

cat /tmp/oix-full-snapshot-latest.dat | grep -iv "0.0.0.0" | awk 'FNR > 5 { print $(NF-1)","$2 }' |
grep -iv { | uniq > /etc/pmacct/netmap.txt

echo "Prefix update finished"