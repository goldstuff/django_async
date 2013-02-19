from async_image_save.tasks import async_save


def save_image(imagefield_data, instance):
    #deconstruct the file into something celery can pickle and send to the worker
    data = {}
    #file is a list containing all info needed to recontruct a UploadedFile object, in the correct order into which they have to
    #be passed to __init__
    file_info = []
    #name of the form field
    file_info.append(imagefield_data.field_name)
    #name of the image
    file_info.append(imagefield_data.name)
    file_info.append(imagefield_data.content_type)
    file_info.append(imagefield_data.size)           
    file_info.append(imagefield_data.charset)
    #the actual data of the image, read into a string
    data['data'] = imagefield_data.read()
            
    #send the image to be saved by a worker
    async_save.delay(data, file_info, instance.__class__, instance.pk)
