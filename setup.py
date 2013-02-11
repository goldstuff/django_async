from distutils.core import setup
import image_upload

long_description = open('README').read()

setup(
    name='django-async',
    version=0.1,
    packages=['image_upload',],
    description='a simple app to asynchronously upload images with Django, using Celery',
    long_description=long_description,
    author='Gregory Terzian',
    author_email='gregory.terzian@gmail.com',
    license='BSD License',
    url='https://github.com/gterzian/django_async.git',
    platforms=["any"],
    requires=['django', 'django-celery', 'pil'],
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)