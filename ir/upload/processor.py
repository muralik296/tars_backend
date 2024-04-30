import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def processText(unProcessedText):
    ''' Returns processed text after removal of stop words and special characters '''

    # replaces new lines with space
    clean_text = unProcessedText.replace('\n', ' ')

    # make all text lowercase => this is to keep it uniform even when user queries
    clean_text = clean_text.lower()

    # remove all special characters from the string
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', clean_text)

    # keeps only a single space between each subsring(word) in the main string
    clean_text = re.sub(r'\s+', ' ', clean_text)

    # removes all trailing spaces
    clean_text = clean_text.strip()

    # remove stop words
    clean_text = remove_stop_words(clean_text) # NO REMOVAL OF STOP WORDS
    return clean_text


# helper fn to remove stop words
def remove_stop_words(text):
    ''' Removes stop words from text '''
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(text)
    # converts the words in word_tokens to lower case and then checks whether
    # they are present in stop_words or not
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    # with no lower case conversion
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    clean_text = ' '.join(filtered_sentence)
    print('clean text = ', clean_text)
    return clean_text
