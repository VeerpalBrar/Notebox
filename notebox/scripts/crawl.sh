#!/bin/bash

current_date_time=$(date)
echo "$current_date_time : Starting crawler"
cd /Users/veerpalbrar/notebox
source ./notebox/elastic/venv/bin/activate
python3 -m notebox.crawler.crawler
# ensure launchd doesn't think the job crashed due to fast run
sleep 10 
echo "ending crawler"