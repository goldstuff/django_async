from distutils.core import setup
import async_image_save

long_description = open('README.rst').read()

setup(
    name='django-async-gt',
    data_files=[('', ['requirements.txt', 'README.rst', 'LICENSE', 'MANIFEST', '.gitignore']),],
    version='0.2',
    packages=['async_image_save',],
    description='a simple app to asynchronously upload images with Django, using Celery',
    long_description=long_description,
    author='Gregory Terzian',
    author_email='gregory.terzian@gmail.com',
    license='BSD License',
    url='http://github.com/gterzian/django_async.git',
    platforms=["any"],
    requires=['django', 'celery', 'pil'],
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)