django-async
=============

:Author: Gregory Terzian
:License: BSD

A simple Django app to store images in async fashion using Celery.
As you cannot pass as image to a Celery task, this app deconstructs the UploadedFile instance, passes it to a Celery task and reconstructs it there.
Finally saving the uploaded image.


License
-------

All code is under a BSD-style license, see LICENSE for details.

Source: http://github.com/duointeractive/django-athumb

Requirements
------------

* python >= 2.7
* django >= 1.4
* Celery >= 3.0
* PIL >= 1.1.6

Installation
------------

To install run::

    pip install django-async


Configuration
-------------

You first of all need to have django-celery set up in your project.

settings.py
^^^^^^^^^^^

Add to ``INSTALLED_APPS``::

    'async_image_save'
    

How to use it in your project
-----------------------------

The functionalities of this app reside in the save_image function, to be used in your views as such::

from async_image_save import save_image

def example_view(request):
    if request.method == "POST":
        form = YourModelForm(request.POST, request.FILES)
        if form.is_valid():
        
            #assuming your model has a main_photo ImageField       
            #save the instance without an image      
            instance = form.save(commit=False)
            instance.main_photo = None
            instance.save()
            instance.users.add(request.user.userprofile)
            
            #send the image to be saved by a worker
            save_image(form.cleaned_data['main_photo'], instance)
            
            return HttpResponseRedirect(reverse('home'))
    else:        
        form = YourModelForm()
    context['form'] = form
    return render_to_response("home.html", context, context_instance=RequestContext(request))
