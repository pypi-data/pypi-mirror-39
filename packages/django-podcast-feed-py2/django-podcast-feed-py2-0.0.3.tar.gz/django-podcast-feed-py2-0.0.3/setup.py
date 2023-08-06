from setuptools import setup, find_packages
from codecs import open

VERSION = '0.0.3'
NAME = 'django-podcast-feed-py2'
DESCRIPTION = 'Generate Apple Podcasts-compatible syndication feeds.'

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    keywords='django podcast feed',
    version=VERSION,
    license='MPL 2.0',

    author='Ben Jeffrey',
    author_email='mail@benjeffrey.net',
    url='https://github.com/jeffbr13/xq',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Framework :: Django',
    ],

    packages=find_packages(),

    install_requires=[
        'django'
    ],
)
