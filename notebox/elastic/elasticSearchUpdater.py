from notebox.elastic.elasticClient import ElasticClient


class ElasticSearchUpdater:
    def __init__(self):
        self.client =  ElasticClient()
    
    def updateFromChanges(self, changes):
        for file in changes["newFiles"]:
            self.client.createDocument(self.getId(file), self.getFileContent(file))
        
        for file in changes["modifiedFiles"]:
            self.client.updateDocument(self.getId(file), self.getFileContent(file))
        
        for file in changes["deletedFiles"]:
            self.client.deleteDocument(self.getId(file))
    
    def getId(self, file):
        return file.path

    def getFileContent(self, file):
        with open(file.path, 'r') as f:
            text = f.read()
        
        return text