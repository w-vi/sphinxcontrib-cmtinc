# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains a comment extractor _Sphinx_ extension.

.. _Sphinx: http://sphinx.pocoo.org/

comment-include is a reStructuredText_ directive to allow extraction of rst formatted comments from source files.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

This extension adds the ``include-comment`` directive that automatically extracts 
the comments begining with ``/**`` and creates valid entries
for the Sphinx_ writer used to generate the documentation.

Usage example::

    .. include-comment:: file.h
'''

requires = ['Sphinx>=1.0']

setup(
    name='sphinxcontrib-cmtinc',
    version='0.1',
    url='http://packages.python.org/sphinxcontrib-cmtinc/',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-cmtinc',
    license='BSD License',
    author='Vilibald W.',
    author_email='vilibald@wvi.cz',
    description='Include comments from source file Sphinx extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
