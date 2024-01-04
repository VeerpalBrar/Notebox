class Directory:
    def __init__(self, path, files):
        self.path = path
        self.files = files

    def __str__(self):
        files = list(map(lambda f: str(f),  self.files))
        return f'path: {self.path}, files: {files}'
    
    def getChanges(self, other):
        if other == None:
           {"newFiles": self.files} 
           
        if self.path != other.path:
            raise("Directory must share same path")
        
        newFiles = []
        deletedFiles = []
        modifiedFiles = []

        otherFiles = {}
        selfFiles = {}
        for file in other.files:
            otherFiles[file.path] = file
        
        for file in self.files: 
            selfFiles[file.path] = file
            
            if file.path not in otherFiles:
                deletedFiles.append(file)
                continue

            otherFile = otherFiles[file.path]
            if otherFile.lastModifiedAt > file.lastModifiedAt:
                modifiedFiles.append(otherFile)

        for file in other.files:
            if file.path not in selfFiles:
                newFiles.append(file)
        
        return {
            "newFiles": newFiles,
            "deletedFiles": deletedFiles,
            "modifiedFiles": modifiedFiles
        }
            
        
