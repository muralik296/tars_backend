def return_docs(posting_list,phrase_query):
    tokens_in_phrase = phrase_query.split(' ')
    # Initialize the list of document IDs containing the first word
    if tokens_in_phrase[0] in posting_list:
        common_documents = posting_list[tokens_in_phrase[0]]
    else:
        common_documents = {}

    # Find common documents for all terms, focusing on documents first
    for term in tokens_in_phrase[1:]:
        if term in posting_list:
            term_documents = posting_list[term]
            common_documents = {
                doc: common_documents[doc] for doc in common_documents if doc in term_documents}
        else:
            common_documents = {}
            break

    # Now extract positions for these common documents
    document_positions = {}
    for doc in common_documents:
        document_positions[doc] = [posting_list[term][doc]
                                for term in tokens_in_phrase if doc in posting_list[term]]

    print("Documents and their term positions:", document_positions)

    # checking if their positions are next to each other.
    final_documents = {}

    for key,array in document_positions.items():
        is_sequential = True
        for i in range(0,len(array)-1):
            ele = array[i][0]
            next_ele = array[i+1][0]
            if (next_ele - ele != 1):
                is_sequential = False
                break
        if (is_sequential == True):
            final_documents[key] = array

    print(final_documents)
    return final_documents