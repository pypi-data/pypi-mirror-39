from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yandex-translater',
    version='6.0',
    description='API for Yandex Translate',
    url='https://pypi.org/project/yandex-translater/',
    author='James Axl',
    author_email='axlrose112@gmail.com',
    long_description=long_description,
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
          'requests',
      ],
    keywords='yandex-translater translater yandex translate',
    packages=find_packages(exclude=['examples', 'yandex_test.py']),
)

