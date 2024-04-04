# Notebox
Notebox is a tool that indexes files on your computer into ElasticSearch, enabling you to search across all files
via an API. 

Optionally, it can be used alongside my [notebox-search obsidian plugin](https://github.com/VeerpalBrar/notebox-search) to search your obsidian vault. 

# Requirements
- ElasticSearch
- tesseract (for parsing text from images)
- python 3  
- 

# Installation 
## Download requirements 
1. [Download and install ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html) and have it running so notebox and index files.
2. [Download and install tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)
3. Download this repository via git clone. 
4. Install required packages with `pip install -r requirements.txt`  
5. Create a .env file which will contain the required configuration params. See notebox/sample.env for format and keys. This will specify how to connect to elastic search and which folder notebox will index. 

## Run Manually 
1. use `python3 -m notebox.crawler.crawler` to crawl all files in the folder specified in the .env file. 
2. use `python3 -m flask --app notebox/server run --port 8070` to run the server. 
3. You can use `curl http://127.0.0.1:8070/search?txt=query` to search all files for certain text. 

Logs for the crawler are saved to `notebox/logs`. 
## Setup background jobs 
On mac, Notebox can be set up to run in the background using [launch agents](/notebox/scripts/). 
1. The crawler will be started with the `notebox/scripts/crawl.sh` file. Modify this file to `cd` into your local notebox folder. 
1. Copy `notebox/scripts/local.notebox.crawler.start.plist` to `~/Library/LaunchAgents/`
2. Copy `notebox/scripts/local.notebox.server.start.plist` to `~/Library/LaunchAgents/`
3. Load and start the launch agents with:
```
launchctl load -w ~/Library/LaunchAgents/local.notebox.crawler.start.plist
launchctl start local.notebox.crawler.start.plist

launchctl load -w ~/Library/LaunchAgents/local.notebox.server.start.plist
launchctl start local.notebox.server.start.plist
```
Now, the crawler will run every hour to index your files. The server will be running and available for API calls.

Logs for the crawler are saved to `notebox/logs` and logs for the server are saved to `notebox/scripts/logs`.  

# Running Tests
From the root folder, run `python3 -m unittest discover -p *Test.py` to run all unit tests. 

# Design 
## Crawler 
The [crawler](/notebox/crawler/crawler.py) is responsible for walking the file tree and finding all text and image files in a directory (and any subdirectories). It relies on pythons built in `os.walk` library. 

All files are passed to the Syncer. 

## Syncer
The [Syncer](/notebox/sync/sync.py) is the core logic of notebox. Given files from the crawler, the syncer will sync them all to elastic search. 

The syncer has an [internal model](/notebox/sync/directoryLookup.py) of the file tree stored in mongo DB. It uses this [internal tree](/notebox/shared/directory.py) to determine which files have been added since the last sync, which have been modified, and which have been deleted. It then updates [elastic search](/notebox/elastic/elasticSearchUpdater.py) to also create, update, and delete files. 

The entirety of a text files contents are stored in elastic search. For image files, notebox uses [tesseract](/notebox/extractor/textExtractor.py) to extract text from the image, and stores the extract text in elastic search. 

## Server
The [server](/notebox/server/search.py) is a small API which allows the user to search for a string of text across their files. The server queries elastic search for this text, searching both file contents and file titles. 

The server returns an array of results which includes the file path and a small extract from the file where the string was found. 

# Future Improvements
Here is a list of missing feature or improvements that may be added in the future:
- Server authentication
- script to automate most if not all of the setup
- Add pagination to server APIs