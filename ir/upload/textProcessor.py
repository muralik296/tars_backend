import re


def processText(unProcessedText):
    ''' Returns processed text '''
    # replaces new lines with space
    resultText = unProcessedText.replace('\n', ' ')

    # make all text lowercase => this is to keep it uniform even when user queries
    resultText = resultText.lower()

    # remove all special characters from the string
    resultText = re.sub(r'[^a-zA-Z0-9\s]', '', resultText)


    # keeps only a single space between each subsring(word) in the main string
    resultText = re.sub(r'\s+', ' ', resultText)

    # removes all trailing spaces
    resultText = resultText.strip()

    return resultText
