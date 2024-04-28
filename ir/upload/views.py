from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import datetime

# used to determine file extensions
from . import handlers
from .processor import processText
from .ElasticCloud import elasticCloud
from . import helpers

# import the creating positional index
from .createPostingsList import createPostingList


# elastic cloud helpers
from .ElasticCloud import main
from .ElasticCloud import positional_index


# upload endpoint
@csrf_exempt
def uploadHandler(request):

    if (request.method == 'POST'):
        print('Post requst')

        # check if the request body to the uplaod handler are files =>
        # if files we are going to handle files in the below manner

        # if the request contains files, then we are going to check for the file type
        # based on the extension.

        # if the extension is pdf => we would use extract pdf to get the text out of it.

        if (request.FILES):
            print(request.FILES)
            uploaded_files = request.FILES.getlist('files')
            print(uploaded_files)

            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name
                # save the file in the server
                saved_path = default_storage.save(file_name, uploaded_file)
                print(saved_path, '= saved path')

                relative_path = f'/media/{saved_path}'
                absolute_path = default_storage.path(saved_path)

                fileExtension = helpers.getFileExtension(absolute_path)
                print(fileExtension)
                print(file_name, '= name of file')
                print(absolute_path, '= absolute path of the file')
                print(relative_path, '= relative path of file')
                print(fileExtension, '= file extension')

                # get type of file from the file format
                typeOfFile = fileExtension.split('/')[1]

                # pdf handler
                if (typeOfFile == 'pdf'):
                    # call the pdf handler function to get the text from the pdf
                    text = handlers.getTextFromPDF(absolute_path)

                # image handler
                elif (typeOfFile in ['png', 'jpg', 'jpeg']):
                    text = handlers.getTextFromImage(absolute_path)

                # text handler
                elif (typeOfFile == 'plain'):
                    text = handlers.getTextFromTextFile(absolute_path)

                # .docx file handler
                elif ('wordprocessingml' in typeOfFile):
                    text = handlers.getTextFromWordDocument(absolute_path)

                elif (typeOfFile == 'html'):
                    text = handlers.getTextFromHtmlFile(absolute_path)

                else:
                    # TO DO : Throw error non supported file
                    pass

                # processed text after getting text from the handler
                processedText = processText(text)

                # generate document id
                documentid = str(uuid.uuid4())

                print(processedText)

                document = {
                    'documentid': documentid,
                    'file_name': file_name,
                    'file_loc': relative_path,
                    'content': processedText,
                    'type': 'image' if typeOfFile in ['png', 'jpg', 'jpeg'] else typeOfFile,
                    'created_at': datetime.datetime.now().isoformat()
                }

                # insert each document into the main table
                res = main.insert_into_main(document)
                print(res, '= from insertion')

                # Now once we have the document in our main table, we need to create a positional index or update existing positional index 

                # seeing if positional index already exists by fetching 
                positionalIndexResult = positional_index.get_positional_index()

                print(positionalIndexResult)

                oldPostingListResults = positionalIndexResult['hits']['hits']

                # checking to see if positional index exists
                if (len(oldPostingListResults) == 0):
                    # if the positional index is not there, create one
                    print('not exists')
                    # create the positional index
                    posting_list = createPostingList(processedText, documentid)
                    print(posting_list, '= posting list')
                    # save the positional index
                    res = positional_index.insert_into_positional_index_index(
                        posting_list)

                    print(res, '= from elastic cloud')

                else:
                    # TO DO: Create a posting list for all existing documents and merge into the old one
                    # Right now inefficiently making read/write from the elastic cloud db

                    print('exists')

                    print(positionalIndexResult,
                        '= raw results from elastic cloud')

                    # use this to update with new positional index
                    # gives the stored id of positional index
                    id = oldPostingListResults[0]['_id']
                    oldPostingList = oldPostingListResults[0]['_source']['positional_index']

                    # create new posting list from the existing posting list
                    newPostingList = createPostingList(
                        processedText, documentid, oldPostingList)

                    print(newPostingList)

                    doc = {
                        'positional_index': newPostingList
                    }

                    # update the posting list
                    res = positional_index.update_positional_index(id, doc)

        # # URL Handler
        # elif (request.POST['urls']):
        #     # TO DO support for urls and scrape data
        #     pass

        return JsonResponse({
            'msg': 'success'
        })
