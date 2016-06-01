#!/bin/bash

# 1. Download all years from 1960-2015 by decades
mkdir -p regular_season/archives
cd regular_season
wget http://www.retrosheet.org/events/1960seve.zip
wget http://www.retrosheet.org/events/1970seve.zip
wget http://www.retrosheet.org/events/1980seve.zip
wget http://www.retrosheet.org/events/1990seve.zip
wget http://www.retrosheet.org/events/2000seve.zip
wget http://www.retrosheet.org/events/2010seve.zip
mkdir events
mkdir box_scores
unzip \*.zip -d events
mv *.zip archives
cd ..

# 2. Download all postseason data
mkdir -p postseason/archives
cd postseason
wget http://www.retrosheet.org/events/allpost.zip
mkdir events
mkdir box_scores
unzip allpost.zip -d events
mv *.zip archives
cd ..

# 3. Use Chadwick to build box scores
export LD_LIBRARY_PATH=/usr/local/lib
./build_box_scores.py

# 4. Parse the box scores and extract all pitcher starts
../parse.py
