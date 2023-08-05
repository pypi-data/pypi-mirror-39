#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-cindy',
    url='https://bitbucket.org/lullis/django_cindy',
    version='0.0.3',
    packages=find_packages(exclude=['test_project']),
    include_package_data=True,
    install_requires=[
        'celery',
        'dateparser',
        'django>=2.0',
        'django-boris',
        'django-model-utils',
        'django-taggit',
        'feedparser',
        'psycopg2-binary',
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
    keywords='django syndication feed-parsing readability'
)
