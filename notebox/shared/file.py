import os 
class File:
    def __init__(self, path, lastModifiedAt):
        self.path = path
        self.lastModifiedAt = lastModifiedAt

    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self):
        return f'path: {self.path}, lastModified: {self.lastModifiedAt}'
    
    def isTextFile(self):
        name = os.path.splitext(self.path)
        return name[1] in [".md", ".txt"]
    
    def isImageFile(self):
        name = os.path.splitext(self.path)
        return name[1] in [".jpg", ".png"]