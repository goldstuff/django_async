django-async
=============

:Author: Gregory Terzian
:License: BSD

A package of Django apps for common async tasks using Celery. For now only one app, used for saving an uploaded image with a Celery worker.

async_image_save
----------------

As you cannot pass as image to a Celery task, this app deconstructs the UploadedFile instance, passes it to a Celery task and reconstructs it there.
Finally saving the uploaded image.


License
-------

All code is under a BSD-style license, see LICENSE for details.

Source: https://github.com/gterzian/django_async.git

Requirements
------------

* python >= 2.7
* django >= 1.4
* Celery >= 3.0
* PIL >= 1.1.6

Installation
------------

To install run::

    pip install django-async-gt


Configuration
-------------

You first of all need to have django-celery set up in your project.

settings.py
^^^^^^^^^^^

Add to ``INSTALLED_APPS``::

    'async_image_save'


About Django and image upload
-----------------------------

Django uploads images and other files in the form of UpLoadedFile objects.
UpLoadedFile is the abstract baseclasse, while TemporaryUploadedFile and InMemoryUploadedFile are the built-in concrete subclasses.
An UploadedFile object behaves somewhat like a file object and represents some file data that the user submitted with a form.

The uploadedfile is received in the view as part of request.FILES, which you will usually bind to a form.
Running the form's is_valid method will then validate this file, or in the case of an ImageField whether the fiel is an actual image, and return the UpLoadedFile object for you to use,
as either a TemporaryUploadedFile and InMemoryUploadedFile.

Once Django form validation has been succesfully run, you can safely assume that you are dealing with an actual image. The normal course of business is to immediatly bind the uploaded file object
to a model, but this means saving the image to your data store while the client is still waiting for a response from the server.

Wouldn't it be better to pass the image along to a celery worker to save in the background?

The problem is that Celery needs to be able to pickle objects to pass them along to workers, and it cannot pickle a file like object.

The remaining option is to deconstruct the file object, write it's data into a string and taking all the other info that you need.
This data can be pickled and therefore passed on to Celery. You then simply need to reconstruct an actual emporaryUploadedFile and InMemoryUploadedFile on the other end,
and bind this object to an instance of a model, by passing the id of that instance along with all other  raw file 'data'. 

Read the docs
UploadedFile: https://docs.djangoproject.com/en/1.4/topics/http/file-uploads/#django.core.files.uploadedfile.UploadedFile
Binding data to forms: https://docs.djangoproject.com/en/1.4/ref/forms/api/#binding-uploaded-files

How to use it in your project
-----------------------------

The functionalities of this app reside in the save_image function, to be used in your views like the below.

::

    from async_image_save.utils import save_image

    def example_view(request):
        if request.method == "POST":
            form = YourModelForm(request.POST, request.FILES)
            if form.is_valid():
                # assuming your model has a main_photo ImageField       
                # save the instance without an image      
                instance = form.save(commit=False)
                instance.main_photo = None
                instance.save()
                instance.users.add(request.user.userprofile)
                # send the image to be saved by a worker
                save_image(form.cleaned_data['main_photo'], instance)
            
                return HttpResponseRedirect(reverse('home'))
        else:        
            form = YourModelForm()
        context['form'] = form
        return render_to_response("home.html", context, context_instance=RequestContext(request))
