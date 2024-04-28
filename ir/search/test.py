posting_list = {
    "machine": {
        "8be0f082-fe6e-4f89-aaf1-68070a559972": [
            5
        ],
        "844ba786-4f0f-4c1f-960c-73c1148df335": [
            7
        ]
    },
    "learning": {
        "8be0f082-fe6e-4f89-aaf1-68070a559972": [
            6
        ],
        "2d6999c1-9120-4a11-866e-4be6dad9e895": [
            8
        ],
        "844ba786-4f0f-4c1f-960c-73c1148df335": [
            1
        ]
    },
    "fundamental": {
        "8be0f082-fe6e-4f89-aaf1-68070a559972": [
            2
        ]
    },
    "making": {
        "2d6999c1-9120-4a11-866e-4be6dad9e895": [
            0
        ]
    },
    "learn": {
        "2d6999c1-9120-4a11-866e-4be6dad9e895": [
            2
        ],
        "844ba786-4f0f-4c1f-960c-73c1148df335": [
            3
        ]
    },
    "machines": {
        "2d6999c1-9120-4a11-866e-4be6dad9e895": [
            1
        ]
    },
    "right": {
        "844ba786-4f0f-4c1f-960c-73c1148df335": [
            4
        ]
    },
    "fun": {
        "844ba786-4f0f-4c1f-960c-73c1148df335": [
            2
        ]
    }
}


# phrase_query = 'machine learning'

# tokens_in_phrase = phrase_query.split(' ')
# print(tokens_in_phrase)
# l = []  # this array will consist of only phrase query posting list
# for key in tokens_in_phrase:
#     l.append(posting_list[key])
# print(l)

# filtered_list = []

# for i in range(0,len(l)-1):
#     element = l[i]
#     next_element = l[i+1]
#     for j in element.keys():
#         if (j in next_element.keys() and (j not in filtered_list)):
#             filtered_list.append(j)

# # need to find the intersection to get the documents
# print(filtered_list)


phrase_query = 'machine learning'
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
