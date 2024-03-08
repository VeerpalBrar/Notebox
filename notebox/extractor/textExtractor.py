import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

class TextExtractor:
    def getFileContents(self, file):
        if file.isTextFile():
            return self.readFileContents(file)
        elif file.isImageFile():
            return self.parseTextFromImage(file)
        
        return ''
    
    def readFileContents(self, file):
        with open(file.path, 'r') as f:
            text = f.read()
        
        return text  

    def parseTextFromImage(self, file):
        return pytesseract.image_to_string(file.path) 
        

