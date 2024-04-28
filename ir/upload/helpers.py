import magic

def getFileExtension(file):
    ''' Returns file extension of a file'''
    mimeType = magic.from_file(file, mime = True)
    return mimeType