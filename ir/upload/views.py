from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import datetime;

# used to determine file extensions
from . import utils

from . import textProcessor

from . import googleVision

from .ElasticCloud import elasticCloud


client = elasticCloud.client
index = 'ir_project'


print(client.info())


@csrf_exempt
def uploadHandler(request):
    if (request.method == 'GET'):
        return JsonResponse({
            'msg': 'upload'
        })
    elif (request.method == 'POST'):
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

                fileExtension = utils.getFileExtension(absolute_path)
                print(file_name, '= name of file')
                print(absolute_path, '= absolute path of the file')
                print(relative_path, '= relative path of file')
                print(fileExtension, '= file extension')

                # get type of file from the file format
                typeOfFile = fileExtension.split('/')[1]

                # pdf handler
                if (typeOfFile == 'pdf'):
                    # call the pdf handler function to get the text from the pdf
                    text = utils.getTextFromPDF(absolute_path)

                # image handler
                elif (typeOfFile in ['png', 'jpg', 'jpeg']):
                    text = googleVision.fetchImageData(absolute_path)

                # text handler
                elif (typeOfFile == 'plain'):
                    file = open(absolute_path, "r")
                    text = file.read()

                # TO DO: To build a positional index on unprocessed text
                # this way we get the exact position of these terms from the unprocessed text

                # processed text after getting text from the handler
                processedText = textProcessor.processText(text)

                print(processedText)

                # here we store the below format in elastic search cluster (data ingestion)
                # documentid, file_name, file_location, content(processed text), positional indices of each term,type
                res = client.index(
                    index=index,
                    document={
                        'documentid': uuid.uuid4(),
                        'file_name': file_name,
                        'file_loc': relative_path,
                        'content': processedText,
                        'type': 'image' if typeOfFile in ['png', 'jpg', 'jpeg'] else typeOfFile,
                        # 'position_index': position_index,
                        'created_at': datetime.datetime.now().isoformat()
                    })
                print(res, '= from insertion')
                client.indices.refresh(index=index)
        elif (request.POST['urls']):
            # TO DO support for urls and scrape data
            pass

        return JsonResponse({
            'msg': 'success'
        })
