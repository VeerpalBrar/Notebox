from ..shared.logger import logging
from ..elastic.elasticSearchUpdater import ElasticSearchUpdater
from .directoryLookup import DirectoryLookup
from ..shared.directory import Directory

logger = logging.getLogger('notebox.sync')
class Sync:
    def __init__(self):
        self.directoryLookup = DirectoryLookup() 
        self.elasticSearchUpdater = ElasticSearchUpdater()
    
    def syncDirectory(self, root, allFiles, initial):
        if initial:
            self.syncFullDirectory(root, allFiles)
        else:
            self.syncChanges(root, allFiles)

    def syncChanges(self, root, allFiles):
        oldFilesInDirectory = self.directoryLookup.getStoredDirectoryContents(root)
        newFilesInDirectory = Directory(root, allFiles)
        changes = oldFilesInDirectory.getChanges(newFilesInDirectory)
        logger.info("Syncing changes. Found {} new file, {} deleted files, {} modified files".format(
            len(changes["newFiles"]),
            len(changes["deletedFiles"]),
            len(changes["modifiedFiles"])
        ))
        self.elasticSearchUpdater.updateFromChanges(changes)
        self.directoryLookup.save(newFilesInDirectory)
 
    def syncFullDirectory(self, root, allFiles):
        changes = {
            "newFiles": allFiles,
            "deletedFiles": [],
            "modifiedFiles": [],
        }
        newFilesInDirectory = Directory(root, allFiles)
        self.elasticSearchUpdater.updateFromChanges(changes)
        self.directoryLookup.save(newFilesInDirectory)
 

        

    
