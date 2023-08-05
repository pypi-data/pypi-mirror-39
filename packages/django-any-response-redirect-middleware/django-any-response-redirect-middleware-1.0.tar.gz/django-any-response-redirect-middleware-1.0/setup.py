#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(name='django-any-response-redirect-middleware',
      version='1.0',
      description="A subclass of Django's RedirectFallbackMiddleware that will catch any response code, not just 404s.",
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
      author='Ryan Bagwell',
      author_email='ryan@ryanbagwell.com',
      url='https://github.com/ryanbagwell/django-any-response-redirect-middleware/',
      packages=find_packages(),
      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
      ],
      install_requires=[
        'django',
      ]
)
