import os
import io

# Imports the Google Cloud client library
from google.cloud import vision

# the json file containing api credentials to talk to google vision api
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/maneendra/Desktop/ir/ir/upload/secrets.json'


def fetchImageData(imagePath):

    resultingTextFromImage = ''

    with io.open(imagePath, 'rb') as image_file:
        content = image_file.read()
    """Provides a quick start example for Cloud Vision."""

    client = vision.ImageAnnotatorClient()  

    image = vision.Image(content=content)

    responseLabels = client.label_detection(image=image)
    
    
    # grabs labels from image
    for label in responseLabels.label_annotations:
        resultingTextFromImage = resultingTextFromImage + label.description + ' '

    # grabs text from image
    responseText = client.text_detection(image=image)
    for r in responseText.text_annotations:
        resultingTextFromImage = resultingTextFromImage + r.description + ' '

    return resultingTextFromImage

