# -*- coding: utf-8 -*-
"""
    sphinxcontrib.c-include
    ~~~~~~~~~~~~~~~~~~~~~~~

    Extract comments from c/c++ sources. Comments object and function signatures.
 
    See the README file for details.

    :author: Vilibald W. <vilibald@wvi.cz>
    :license: MIT, see LICENSE for details
"""

import posixpath
from os import path
from docutils import nodes
from sphinx.util.nodes import nested_parse_with_titles
from docutils.statemachine import ViewList
from docutils.parsers.rst import directives
from sphinx.application import ExtensionError
from sphinx.util.compat import Directive
from sphinx.errors import SphinxError


class CIncludeError(SphinxError):
    category = 'AutoDocJS  error'

            
class CIncludeDirective(Directive):
    """
    Directive to insert comments and signatures form C/C++ source file.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = { }

    def run(self):
        self.reporter = self.state.document.reporter
        self.env = self.state.document.settings.env
        if self.arguments:
            if self.content:
                return self.reporter.warning(
                    'c-include directive cannot have content only '
                    'a filename argument', line=self.lineno)
            rel_filename, filename = self.env.relfn2path(self.arguments[0])
            self.env.note_dependency(rel_filename)
            try:
                return self.module(filename)
            except (IOError, OSError):
                return self.reporter.warning(
                    'External C/C++ file %r not found or reading'
                    'failed' % filename, line=self.lineno)

    def module(self, src):
        """
        Process whole C/C++ source file.
        """
        extractor = extractor.Extractor()
        try:
            with open(src, 'r') as f:
                extractor.extract(f))
        except extractor.ExtractError as e:
                msg = self.reporter.warning(
                    'Extraction error in external C/C++ file %r : %s'
                    % (src, str(e)), line=self.lineno)
                return [msg]

        self.content = extractor.content
        self.content_offset = 0
        # Create a node, to be populated by `nested_parse`.
        node = nodes.compound(rawsource='')
        # Parse the directive contents.
        nested_parse_with_titles(self.state, self.content, node)
        return node.children

def setup(app):

    app.add_directive('c-include', CIncludeDirective)

