# text = 'i am here now where are you you here'
# id = 1


def createPostingList(text, document_index, term_index={}):
    """ Takes the content and document id and creates a positional index """
    splittedText = text.split(" ")
    for index, term in enumerate(splittedText):
        # print(term, index)

        # for each term we are trying to check if the term is present in the term_index dictionary, otherwise we are
        # creating a blank dictionary for the term.

        if term_index.get(term, 0) == 0:
            term_index[term] = {}

        # Next, we are checking if a document id is present in the term dictionary. if it's not there, we are storing
        # the index of the term in the list, so as to create a posting list for each term. Because we are using dictionaries
        # we will have a nested structure where for each term we will have a collection of keys which are doc ids.

        if document_index not in term_index[term]:

            term_index[term][document_index] = [index]

        else:
            term_index[term][document_index].append(index)

    return term_index


# oldPostingList = createPostingList(text, id)
# print(oldPostingList)
# newText = 'i am the world babe where are you'
# newPostingList = createPostingList(newText, 2, oldPostingList)
# print(newPostingList)
def merge_posting_lists(old_list, new_list):
    # Iterate over each term and the corresponding docs in the new posting list
    for term, new_docs in new_list.items():
        if term in old_list:
            # If the term is already in the old list, just update with new docs
            old_list[term].update(new_docs)
        else:
            # If the term is not in the old list, add it along with its documents
            old_list[term] = new_docs
    return old_list
