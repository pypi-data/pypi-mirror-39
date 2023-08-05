#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-kip',
    url='https://bitbucket.org/lullis/django_kip',
    version='0.0.2',
    packages=find_packages(exclude=['test_project']),
    include_package_data=True,
    install_requires=[
        'celery',
        'django>=2.0',
        'django-model-utils',
        'django_ipfs_storage',
        'psycopg2-binary'
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
    keywords='django ipfs'
)
