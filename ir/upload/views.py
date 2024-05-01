from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
import uuid
import datetime

# used to determine file extensions
from . import handlers
from .processor import processText
from . import helpers

# import the creating positional index
from . import utils


# elastic cloud helpers
from dbutils import main
from dbutils import positional_index
from elasticsearch.exceptions import NotFoundError, ConnectionError, TransportError
import json


# upload endpoint
@csrf_exempt
def uploadHandler(request):
    try:
        current_term_index = {}
        documents = []

        if (request.method == 'POST'):
            
            # FILE HANDLER
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

                    # html file handler
                    elif (typeOfFile == 'html' or typeOfFile == 'htm'):
                        text = handlers.getTextFromHtmlFile(absolute_path)

                    else:
                        # TO DO : Throw error non supported file
                        pass

                    # processed text after getting text from the handler
                    processedText = processText(text)

                    # generate document id
                    documentid = str(uuid.uuid4())

                    print(processedText)

                    # build a term index if not already there in memory
                    if (not current_term_index):
                        print('empty')
                        current_term_index = utils.createPostingList(
                            processedText, documentid)
                    else:
                        print('there')
                        current_term_index = utils.createPostingList(
                            processedText, documentid, current_term_index)

                    document = {
                        "_index": "main",
                        "_id": documentid,
                        "_source": {
                            'documentid': documentid,
                            'file_name': file_name,
                            'file_loc': relative_path,
                            'content': processedText,
                            'type': 'image' if typeOfFile in ['png', 'jpg', 'jpeg'] else typeOfFile,
                            'created_at': datetime.datetime.now().isoformat(),
                            'posting_list':utils.create_term_index_for_text(processedText)
                        }
                    }
                    documents.append(document)

            # URL Handler
            else:
                current_term_index = {}
                documents = []

                request_body = json.loads(request.body)
                print(request_body)
                list_of_urls = request_body['urls']
                print(list_of_urls)

                for element in list_of_urls:
                    url = element['url']
                    documentid = element['urlId']
                    text = handlers.getTextFromWebsite(url)
                    processedText = processText(text)
                    print(processedText)

                    # build a term index if not already there in memory
                    if (not current_term_index):
                        print('empty')
                        current_term_index = utils.createPostingList(
                            processedText, documentid)
                    else:
                        current_term_index = utils.createPostingList(
                            processedText, documentid, current_term_index)
                        
                    document = {
                        "_index": "main",
                        "_id": documentid,
                        "_source": {
                            'documentid': documentid,
                            'file_name': url,
                            'file_loc': None,
                            'content': processedText,
                            'type': 'url',
                            'created_at': datetime.datetime.now().isoformat(),
                            'posting_list':utils.create_term_index_for_text(processedText)
                        }
                    }

                    documents.append(document)

            
            print(current_term_index,
                    '= current term index from the uploaded docs')

            # seeing if positional index already exists by fetching
            isPositionalIndexExist = positional_index.check_document_exists()

            print(isPositionalIndexExist)

            # create new term index if not there
            if (isPositionalIndexExist == False):
                print('--- Term Index NOT EXISTS ----')
                # save the current term index
                res = positional_index.insert_into_positional_index_index(
                    current_term_index)

            # update existing term index with current documents information
            else:
                print('--- Term Index exists ----')
                old_term_index = positional_index.get_positional_index()

                old_term_index = old_term_index['_source']['positional_index']
                print(old_term_index, '= old term index')

                # create new posting list from the existing posting list
                new_term_index = utils.merge_posting_lists(
                    old_term_index, current_term_index)

                print(new_term_index)

                doc = {
                    'positional_index': new_term_index
                }

                # update the posting list
                update_term_index = positional_index.update_positional_index(
                    doc)

            # finally lets also store these uploaded documents information to the main index
            insertion_documents = main.bulk_insert(documents)
            
            return JsonResponse({
                'msg': 'success'
            }, status=201)
        
    except NotFoundError as e:
        print("The document or index specified does not exist.")
        print(e, '= error')
        return JsonResponse({
            'msg': 'Not found'
        }, status=404)
    except Exception as e:
        print(e, 'an error occured')
        return JsonResponse({
            'msg': 'An Error occured, please try again later'
        }, status=500)
