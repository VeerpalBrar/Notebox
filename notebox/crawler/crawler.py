import os
from ..shared.logger import logging
from ..shared.settings import config 
from datetime import datetime, timedelta
from ..shared.file import File
from ..sync.sync import Sync

logger = logging.getLogger('notebox.crawler')
yesterday = datetime.now() - timedelta(days=1)
yesterday = yesterday.timestamp()

START_PATH = config["CRAWLER_START_PATH"]
lastModifiedDate = yesterday
syncer = Sync()
def findModifiedFiles(modifiedSinceTime, files, root):
    modifiedFiles = []
    for fn in files:
        path = os.path.join(root, fn)
        if os.path.getmtime(path) > modifiedSinceTime:
            modifiedFiles.append(path)
    return modifiedFiles

def isNotHiddenFile(path):
    name = os.path.basename(path)
    return name[0] != "."

def isTextFile(path):
    name = os.path.splitext(path)
    return name[1] in [".md", ".txt"]


def isNotHiddenDirectory(path):
    return "." not in path

def createFiles(files, root):
    createdFiles = []
    for fn in files:
        path = os.path.join(root, fn)
        createdFiles.append(File(path, os.path.getmtime(path)))
    return createdFiles


def walk_error_handler(exception_instance):
    print(exception_instance)
    logger.info("{}".format(exception_instance))

def crawl(initial=False):
    logger.info("Starting crawl. Start path={}. Initial={}".format(START_PATH, initial))

    for root, dirs, files in os.walk(START_PATH):
        try:
            logger.info("crawling path: {}".format(root))
            dirs[:] = filter(isNotHiddenDirectory, dirs)
            files = filter(isNotHiddenFile, files)
            files = list(filter(isTextFile, files))
            foundFiles = createFiles(files, root)
            # foundDirs = findModifiedFiles(yesterday, files, root)
            # print(len(foundDirs))
            # for file in foundFiles:
            #     print("f: ", file.path)
            # for dir in foundDirs:
            #     print("d: ", dir)

            syncer.syncDirectory(root, foundFiles, initial)
        except Exception as e:
            print(e)
            logger.error("Error while crawling {}".format(e))
            raise e
    logger.info("Finished crawl")

crawl(initial=False)