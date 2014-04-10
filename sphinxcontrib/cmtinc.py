# -*- coding: utf-8 -*-
"""
    sphinxcontrib.cmtinc
    ~~~~~~~~~~~~~~~~~~~~~~~

    Extract comments from source files. 
 
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
import extractor

class CmtIncDirective(Directive):
    """
    Directive to insert comments form source file.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = { }

    def run(self):
        """Run it """
        self.reporter = self.state.document.reporter
        self.env = self.state.document.settings.env
        if self.arguments:
            if self.content:
                return [self.reporter.warning(
                    'include-comment directive cannot have content only '
                    'a filename argument', line=self.lineno)]
            rel_filename, filename = self.env.relfn2path(self.arguments[0])
            self.env.note_dependency(rel_filename)
            try:
                extr = extractor.Extractor()
                with open(filename, 'r') as f:
                    extr.extract(f)
                self.content = extr.content
                self.content_offset = 0
                # Create a node, to be populated by `nested_parse`.
                node = nodes.paragraph()
                # Parse the directive contents.
                nested_parse_with_titles(self.state, self.content, node)
                return node.children
            except (IOError, OSError, extractor.ExtractError):
                return [self.reporter.error(
                    'External file %r not found or reading '
                    'failed' % filename, line=self.lineno)]
        return [] 
        
def setup(app):
    app.add_directive('include-comment', CmtIncDirective)

