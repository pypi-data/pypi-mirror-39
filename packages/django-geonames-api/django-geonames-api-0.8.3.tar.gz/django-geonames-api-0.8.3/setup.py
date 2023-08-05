import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-geonames-api',
    version='0.8.3',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app to implement the geonames database.',
    long_description=README,
    url='https://www.example.com/',
    author='Nicolas Pieuchot',
    author_email='n.pieuchot@zero-gachis.com',
    install_requires=[
        'django-haystack==2.8.1',
        'django-haystack-elasticsearch5==0.7',
        'django-autocomplete-light==3.3.2',
        'six==1.11.0',
        'django-tastypie==0.14.2'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
