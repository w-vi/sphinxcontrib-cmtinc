# -*- coding: utf-8 -*-

import re
from docutils.statemachine import ViewList

re_comment = re.compile("^\s?/\*\*\**(.*)$")
re_cmtnext = re.compile("^[/\* | \*]?\**(.*)$")
re_cmtend = re.compile("(.*)(\*/)+$")

class ExtractError(Exception):
    pass

class Extractor(object):
    """
    Main extraction class
    """
    
    def __init__(self):
        """
        """    
        self.content = ViewList("",'comment')
        self.lineno = 0

    def extract(self, source):
        """
        Process the source file and fill in the content.
        SOURCE is a fileobject.
        """
        for l in source:
            self.lineno = self.lineno + 1
            l = l.strip()
            m = re_comment.match(l)
            if m:
                self.comment(m.group(1), source)
        
    
    def comment(self, cur, source):
        """
        Read the whole comment and strip the stars.
        CUR is currently read line and SOURCE is a fileobject with the source code.
        """
        if(cur != ""):
            self.content.append(cur.rstrip(), "comment")

        for cur in source:
            self.lineno = self.lineno + 1

            if cur.startswith("/*"):
                raise ExtractError("%d: Nested comments are not supported yet." % self.lineno)

            if re_cmtend.match(cur):
                break
            
            m = re_cmtnext.match(cur)
            if m:
                self.content.append(m.group(1).rstrip(), "comment")
                continue

            self.content.append(cur, "comment")


        self.content.append('\n', "comment")

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: extractor.py <file.c|cpp|h>")
        exit(1)

    ext = Extractor()
    try:
        with open(sys.argv[1], 'r') as f:
            ext.extract(f)
    except ExtractError as e:
        print('Extraction error in external source file %r : %s'
                    % (sys.argv[1], str(e)))
    for line in ext.content:
        print(line)

    
