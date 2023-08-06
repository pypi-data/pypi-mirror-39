import io
import os
import sys
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

DESCRIPTION = "A quick thumbnail creator for python codes"

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(name='pythumbnail',
      version='0.0.3',
      description="A quick thumbnail creator for python codes",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/kevinyang372/py-thumbnail',
      author='Yunfan Yang',
      author_email='yunfan.yang@minerva.kgi.edu',
      license='Apache2',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3'
      ],
      packages=['pythumbnail'],
      )