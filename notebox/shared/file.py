class File:
    def __init__(self, path, lastModifiedAt):
        self.path = path
        self.lastModifiedAt = lastModifiedAt

    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self):
        return f'path: {self.path}, lastModified: {self.lastModifiedAt}'
    