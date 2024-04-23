import magic
# importing required modules 
from pypdf import PdfReader 


def getFileExtension(file):
    ''' Returns file extension of a file'''
    mimeType = magic.from_file(file, mime = True)
    return mimeType

def getTextFromPDF(file):
    ''' Returns the text from a pdf '''
    resultText = ''

    # creating a pdf reader object 
    reader = PdfReader(file) 
    
    
    for i in range(0,len(reader.pages)):

    
        # getting a specific page from the pdf file 
        page = reader.pages[0] 
    
        # extracting text from page 
        text = page.extract_text()
        resultText+=text 
    
    return resultText