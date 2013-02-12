from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.cache import cache
from celery import task
import StringIO

@task()
def async_save(data, file, type, id):
    instance = get_object_or_404(type, pk=id)
    img = StringIO.StringIO(data['data'])
    image = InMemoryUploadedFile(img, *file)
    instance.__dict__[file[0]] = image
    instance.save()
    #invalidate the cache
    cache.clear()
    
    