from cmath import log
from ..shared.logger import logging
from notebox.elastic.elasticClient import ElasticClient

logger = logging.getLogger('notebox.elastic.elasticSearchUpdater')
class ElasticSearchUpdater:
    def __init__(self):
        self.client =  ElasticClient()
    
    def updateFromChanges(self, changes):
        logger.info("Updating elastic search.")
        for file in changes["newFiles"]:
            self.client.createDocument(self.getId(file), self.getFileContent(file))
        
        for file in changes["modifiedFiles"]:
            self.client.updateDocument(self.getId(file), self.getFileContent(file))
        
        for file in changes["deletedFiles"]:
            self.client.deleteDocument(self.getId(file))
        logger.info("Finished updating elastic search.")
    
    def getId(self, file):
        return file.path

    def getFileContent(self, file):
        with open(file.path, 'r') as f:
            text = f.read()
        
        return text