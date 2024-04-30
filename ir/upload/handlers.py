from bs4 import BeautifulSoup
import docx2txt
from pypdf import PdfReader

import os
import io

# Imports the Google Cloud client library
from google.cloud import vision

# file path to directory (upload)
path_to_dir = os.path.dirname(os.path.abspath(__file__))

# sets google vision api credentials to current environment - needs a secrets.json file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{path_to_dir}/secrets.json'

# library for document to text


# beautiful soup
from urllib.request import urlopen

# TXT file handler
def getTextFromTextFile(file_path):
    ''' Returns text from text file, takes absolute path of file as argument '''
    file = open(file_path, "r")
    text = file.read()
    return text


# .DOCX file handler
def getTextFromWordDocument(file_path):
    text_from_word_document = docx2txt.process(file_path)
    return text_from_word_document


# PDF Handler
def getTextFromPDF(file):
    ''' Returns the text from a pdf '''
    resultText = ''

    # creating a pdf reader object
    reader = PdfReader(file)

    for i in range(0, len(reader.pages)):

        # getting a specific page from the pdf file
        page = reader.pages[0]

        # extracting text from page
        text = page.extract_text()
        resultText += text

    return resultText


# Image Handler
def getTextFromImage(file):
    ''' Returns text from image (include labels, ocr) using google vision api credentials, takes file path as argument '''
    resultingTextFromImage = ''

    with io.open(file, 'rb') as image_file:
        content = image_file.read()

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

# HTML File handler


def getTextFromHtmlFile(file_path):
    ''' Returns text from html file  '''
    # Open the HTML file

    # latin-1 is the default charset for html files
    with open(file_path, "r", encoding='latin-1') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


# handler for urls
def getTextFromWebsite(url):
    ''' Returns text from visting a website using beautiful soup '''

    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text
