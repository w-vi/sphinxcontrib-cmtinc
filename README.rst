========================================================
Include comments form source files  extension for Sphinx
========================================================

About
=====

This extension allows to extract valid Sphinx_ formatted comments from source
files.  It extracts any comment starting with ``/**`` double star as is usual
with (java/js/doxygen) doc style comments. It goes through the whole file and
grabs whatever valid comment it finds.

This extension adds the ``include-comment`` directive that automatically
extracts the comments and creates valid entries for the Sphinx_ writer
used to generate the documentation.

You can see the latest documentation at the `sphinxcontrib-cmtinc website`__.

__ http://packages.python.org/sphinxcontrib-cmtinc/

Download
========

You can see all the `available versions`__ at PyPI_.

__ http://pypi.python.org/pypi/sphinxcontrib-cmtinc


Requirements
------------

Sphinx_ version > 1.0

From source (tar.gz or checkout)
--------------------------------

Unpack the archive, enter the sphinxcontrib-comment-icnlude directory and run::

    python setup.py install


Setuptools/PyPI_
----------------

Alternatively it can be installed from PyPI_, either manually downloading the
files and installing as described above or using:

easy_install -U sphinxcontrib-cmtinc


Directly from Git repo
----------------------

Of course it is also possible to build it directly from the
source. The git repo is hosted on
https://bitbucket.org/wvi/sphinxcontrib-cmtinc and any input
is welcome.


Enabling the extension in Sphinx_
---------------------------------

Just add ``sphinxcontrib.cmtinc`` to the list of extensions in the ``conf.py``
file. For example::

    extensions = ['sphinxcontrib.cmtinc']


Usage
=====

``.. include-comment:: <file>``

This will extract any comments starting with ``/**`` in the file ``<file>``.

Example c header.h

.. code-block:: c


    /**
      .. c:type:: my_struct_t

      This is a struct for holding values.
    */
    typedef struct my_struct_s
    {
        int id;
        struct timeval t; 
        void *value;
     }  my_struct_t;

    /**
     .. c:function:: my_struct_t * connect(my_struct_t * m, const char *url)
 
     Connect the client to the server given by *url*.

    */
    my_struct_t * connect(my_struct_t * m, const char *url);

.. include-comment:: ../README.rst


Configuration
-------------

None so far.

TODO
====

* Enable inclusion of just selected comments, what I see as usefull is gathering
  same type objects so it'd be for example possible to firts list data types and then functions.
* Enable signature creation form the source. (Lexers are already in place.)
* Transform the doxygen and other styles to Sphinx_ rst.

.. Links:
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org/
.. _PyPI: http://pypi.python.org/pypi


:copyright: Copyright 2014 by Vilibald W.
:license: BSD, see LICENSE.txt for details.
