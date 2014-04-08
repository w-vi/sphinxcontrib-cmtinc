# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains a c/c++ comment extractor _Sphinx_ extension.

.. _c-include: http://wvi.cz/c-include
.. _Sphinx: http://sphinx.pocoo.org/

c-include_ is a reStructuredText_ directive to allow extraction of rst formatted comments from c/c++
source files.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

This extension adds the ``c-include`` directive that automatically extracts 
the comments begginng with '/**'' and creates valid entries
for the Sphinx_ writer used to generate the documentation.

Usage example::

    .. c-include:: file.c
'''

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-c-include',
    version='0.1',
    url='http://packages.python.org/sphinxcontrib-c-include/',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-c-include',
    license='MIT',
    author='Vilibald W.',
    author_email='vilibald@wvi.cz',
    description='Include C/C++ source comments Sphinx extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: MIT ',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
