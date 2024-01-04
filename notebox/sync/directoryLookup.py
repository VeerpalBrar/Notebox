from pymongo import MongoClient
from ..shared.directory import Directory
from ..shared.file import File
from datetime import datetime, timedelta
class DirectoryLookup:
    def __init__(self, client = MongoClient()):
        self.client = client
        self.database = self.client["notebox"]
        self.directories = self.database["directories"]

    def getStoredDirectoryContents(self, path):
        directory = self.directories.find_one({
           "path": path
        })

        if directory:
            files = list(map(lambda file: File(file[0], file[1]), directory['files']))
            return Directory(directory['path'], files)
            
        return None
    
    def save(self, directory):
        filesUpdate = list(map(lambda file: [file.path, file.lastModifiedAt], directory.files))
        self.directories.update_one(
            {
            "path": directory.path
            }, 
            {"$set": {
                    "path": directory.path,
                    "files": filesUpdate
                }
            },
            upsert=True
        )

##### MANUAL TEST #########
# yesterday = datetime.now() - timedelta(days=1)
# yesterday = yesterday.timestamp()

# DirectoryLookup().save(Directory(
#     "/test/path", 
#     [File("/test/path/a", yesterday)]
# ))

# print(DirectoryLookup().getStoredDirectoryContents("/test/path"))
# print(DirectoryLookup().getStoredDirectoryContents("/test/path/not-exist"))
#### END MANUAL TEST ######