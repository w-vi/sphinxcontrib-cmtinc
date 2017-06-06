# -*- coding: utf-8 -*-
"""
    sphinxcontrib.cmtinc
    ~~~~~~~~~~~~~~~~~~~~~~~

    Extract comments from source files.

    See the README file for details.

    :author: Vilibald W. <vilibald@wvi.cz>
    :license: MIT, see LICENSE for details
"""

import sys
import os.path
import re
import time
from docutils import io, nodes, statemachine, utils
from docutils.utils.error_reporting import SafeString, ErrorString
from docutils.utils.error_reporting import locale_encoding
from docutils.parsers.rst import Directive, convert_directive_function
from docutils.parsers.rst import directives, roles, states
from docutils.parsers.rst.directives.body import CodeBlock, NumberLines
from docutils.parsers.rst.roles import set_classes
from docutils.transforms import misc
from docutils.statemachine import ViewList

re_multilinecomment = re.compile("^\s*\/\*\*.*$")
re_multilinecomment_end = re.compile("(.*)\*\/\ *$")
re_whitespace_content = re.compile("^\s*(?:\*|#|(?:\/\/))?(\s*.*)$")

class IncludeComments(Directive):

    """
    Include content read from a separate source file.

    Content may be parsed by the parser, or included as a literal
    block.  The encoding of the included file can be specified.  Only
    a part of the given file argument may be included by specifying
    start and end line or text to match before and/or after the text
    to be used.

    based on the Include Directives at  http://svn.code.sf.net/p/docutils/code/trunk/docutils/docutils/parsers/rst/directives/misc.py
    and https://github.com/sphinx-doc/sphinx/blob/master/sphinx/directives/other.py
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'literal': directives.flag,
                   'code': directives.unchanged,
                   'encoding': directives.encoding,
                   'tab-width': int,
                   'start-line': int,
                   'end-line': int,
                   'start-after': directives.unchanged_required,
                   'end-before': directives.unchanged_required,
                   # ignored except for 'literal' or 'code':
                   'number-lines': directives.unchanged, # integer or None
                   'class': directives.class_option,
                   'name': directives.unchanged}

    standard_include_path = os.path.join(os.path.dirname(states.__file__),
                                         'include')

    def filterText(self, rawtext):
        includeLine = 0
        filterdText =  ViewList("",'comment')
        identationfactor = 0
        keepwhitespaces = False
        for line in rawtext.split('\n'):
            ignoreLine = False;

            m = re_multilinecomment.match(line)
            if(m):
                includeLine +=1
                ignoreLine = True;

            if (includeLine > 0):
                if("\\toggle_keepwhitespaces" in line):
                    ignoreLine = True
                    keepwhitespaces = not keepwhitespaces

                if (any(tag in line for tag in
                        ["\code", "\multicomment"])):
                   includeLine +=1
                   identationfactor += 1
                   ignoreLine = True;

                if (any(tag in line for tag in
                        ["\endcode", "\end_multicomment"])):
                   includeLine -=1
                   identationfactor -= 1
                   ignoreLine = True;

            m = re_multilinecomment_end.match(line)
            if(m and includeLine > 0):
                filterdText.append('\n','comment')
                includeLine -=1
                ignoreLine = True;

            if (not ignoreLine and includeLine > 0):
                if (identationfactor <= 0 and not keepwhitespaces):
                    linecontent = re_whitespace_content.match(line).group(1)
                    filterdText.append('%s\n' % (linecontent),'comment')
                else:
                    filterdText.append('%s%s\n' % ((' ' * identationfactor), line),'comment')
            #else:
                #filterdText.append( 'D%d %s%s\n' % (includeLine, identation, line),'comment')
        if (includeLine != 0):
            raise self.severe("Comments may not be closed correctly! Open comments: %d" % (includeLine))

        return ''.join(filterdText)

    def run(self):
        """Include a file as part of the content of this reST file."""

        # from sphynx Include Directive in https://github.com/sphinx-doc/sphinx/blob/master/sphinx/directives/other.py
        # type: () -> List[nodes.Node]
        env = self.state.document.settings.env
        if self.arguments[0].startswith('<') and \
           self.arguments[0].endswith('>'):
            # docutils "standard" includes, do not do path processing
            return BaseInclude.run(self)
        rel_filename, filename = env.relfn2path(self.arguments[0])
        self.arguments[0] = filename
        env.note_included(filename)
        #end

        if not self.state.document.settings.file_insertion_enabled:
            raise self.warning('"%s" directive disabled.' % self.name)
        source = self.state_machine.input_lines.source(
            self.lineno - self.state_machine.input_offset - 1)
        source_dir = os.path.dirname(os.path.abspath(source))
        path = directives.path(self.arguments[0])
        if path.startswith('<') and path.endswith('>'):
            path = os.path.join(self.standard_include_path, path[1:-1])
        path = os.path.normpath(os.path.join(source_dir, path))
        path = utils.relative_path(None, path)
        path = nodes.reprunicode(path)
        encoding = self.options.get(
            'encoding', self.state.document.settings.input_encoding)
        e_handler=self.state.document.settings.input_encoding_error_handler
        tab_width = self.options.get(
            'tab-width', self.state.document.settings.tab_width)
        try:
            self.state.document.settings.record_dependencies.add(path)
            include_file = io.FileInput(source_path=path,
                                        encoding=encoding,
                                        error_handler=e_handler)
        except UnicodeEncodeError, error:
            raise self.severe(u'Problems with "%s" directive path:\n'
                              'Cannot encode input file path "%s" '
                              '(wrong locale?).' %
                              (self.name, SafeString(path)))
        except IOError, error:
            raise self.severe(u'Problems with "%s" directive path:\n%s.' %
                      (self.name, ErrorString(error)))
        startline = self.options.get('start-line', None)
        endline = self.options.get('end-line', None)
        try:
            if startline or (endline is not None):
                lines = include_file.readlines()
                rawtext = ''.join(lines[startline:endline])
            else:
                rawtext = include_file.read()
        except UnicodeError, error:
            raise self.severe(u'Problem with "%s" directive:\n%s' %
                              (self.name, ErrorString(error)))
        # start-after/end-before: no restrictions on newlines in match-text,
        # and no restrictions on matching inside lines vs. line boundaries
        after_text = self.options.get('start-after', None)
        if after_text:
            # skip content in rawtext before *and incl.* a matching text
            after_index = rawtext.find(after_text)
            if after_index < 0:
                raise self.severe('Problem with "start-after" option of "%s" '
                                  'directive:\nText not found.' % self.name)
            rawtext = rawtext[after_index + len(after_text):]
        before_text = self.options.get('end-before', None)
        if before_text:
            # skip content in rawtext after *and incl.* a matching text
            before_index = rawtext.find(before_text)
            if before_index < 0:
                raise self.severe('Problem with "end-before" option of "%s" '
                                  'directive:\nText not found.' % self.name)
            rawtext = rawtext[:before_index]

        rawtext = self.filterText(rawtext)
        #if (path == "../examples/neuropil_hydra.c"):
            #raise self.severe('filterd text from %s:\n%s' % (path, rawtext))

        include_lines = statemachine.string2lines(rawtext, tab_width,
                                                  convert_whitespace=True)
        if 'literal' in self.options:
            # Convert tabs to spaces, if `tab_width` is positive.
            if tab_width >= 0:
                text = rawtext.expandtabs(tab_width)
            else:
                text = rawtext
            literal_block = nodes.literal_block(rawtext, source=path,
                                    classes=self.options.get('class', []))
            literal_block.line = 1
            self.add_name(literal_block)
            if 'number-lines' in self.options:
                try:
                    startline = int(self.options['number-lines'] or 1)
                except ValueError:
                    raise self.error(':number-lines: with non-integer '
                                     'start value')
                endline = startline + len(include_lines)
                if text.endswith('\n'):
                    text = text[:-1]
                tokens = NumberLines([([], text)], startline, endline)
                for classes, value in tokens:
                    if classes:
                        literal_block += nodes.inline(value, value,
                                                      classes=classes)
                    else:
                        literal_block += nodes.Text(value, value)
            else:
                literal_block += nodes.Text(text, text)
            return [literal_block]
        if 'code' in self.options:
            self.options['source'] = path
            codeblock = CodeBlock(self.name,
                                  [self.options.pop('code')], # arguments
                                  self.options,
                                  include_lines, # content
                                  self.lineno,
                                  self.content_offset,
                                  self.block_text,
                                  self.state,
                                  self.state_machine)
            return codeblock.run()

        self.state_machine.insert_input(include_lines, path)
        return []


def setup(app):
    app.add_directive('include-comment', IncludeComments)
