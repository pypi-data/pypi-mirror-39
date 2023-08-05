#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-boris',
    url='https://bitbucket.org/lullis/django_boris',
    version='0.0.2-201812060038',
    packages=find_packages(exclude=['test_project']),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'celery',
        'django>=2.0',
        'django-model-utils',
        'filemagic==1.6',
        'html-sanitizer',
        'pillow',
        'psycopg2-binary',
        'readability-lxml',
        'requests'
    ],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
    keywords='django crawling content_extraction readability'
)
