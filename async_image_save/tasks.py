from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.cache import cache
from celery import task
import StringIO

@task()
def async_save(data, file_info, type, id):
    #get the instance
    instance = get_object_or_404(type, pk=id)
    #img is the data of the image read into a StringIO buffer
    img = StringIO.StringIO(data['data'])
    #pass the StringIo, and a list of required args to InMemoryUploadedFile
    image = InMemoryUploadedFile(img, *file_info)
    #add the name of the formfield to the instance's __dict__, and set the image to it. 
    instance.__dict__[file_info[0]] = image
    instance.save()
    #invalidate the cache, this is necessary if you are using Johnny Cache, as adding the image to the instance will not invalidate the cache
    cache.clear()
    
    