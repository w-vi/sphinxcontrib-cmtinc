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
import codecs
from os import path

from docutils import nodes
from sphinx.util.nodes import nested_parse_with_titles
from docutils.statemachine import ViewList
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive
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
            
            extr = extractor.Extractor()
            f = None
            try:
                encoding = self.options.get('encoding', self.env.config.source_encoding)
                codec_info = codecs.lookup(encoding)
                f = codecs.StreamReaderWriter(open(filename, 'rb'),
                                                  codec_info[2], codec_info[3], 'strict')
                extr.extract(f)
            except (IOError, OSError):
                return [document.reporter.warning(
                    'Include file %r not found or reading it failed' % filename,
                    line=self.lineno)]
            except UnicodeError:
                return [document.reporter.warning(
                    'Encoding %r used for reading included file %r seems to '
                    'be wrong, try giving an :encoding: option' %
                    (encoding, filename))]
            except (extractor.ExtractError):
                return [self.reporter.error(
                    'External file %r not found or reading '
                    'failed' % filename, line=self.lineno)]
            finally:
                if f is not None:
                    f.close()
            self.content = extr.content
            self.content_offset = 0
            # Create a node, to be populated by `nested_parse`.
            node = nodes.paragraph()
            # Parse the directive contents.
            nested_parse_with_titles(self.state, self.content, node)
            return node.children
        else:
            return [self.reporter.warning(
                'include-comment directive needs a filename argument', 
                line=self.lineno)]
        
def setup(app):
    app.add_directive('include-comment', CmtIncDirective)

