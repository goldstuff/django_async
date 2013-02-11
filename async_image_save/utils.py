from image_upload.tasks import async_save


def save_image(imagefield_data, instance):
    #deconstruct the file into something celery can pickle and send to the worker
    data = {}
    file = []
    file.append(imagefield_data.field_name)
    file.append(imagefield_data.name)
    file.append(imagefield_data.content_type)
    file.append(imagefield_data.size)           
    file.append(imagefield_data.charset)
    data['data'] = imagefield_data.read()
            
    #send the image to be saved by a worker
    async_save.delay(data, file, instance.__class__, instance.pk)
