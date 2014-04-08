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
        self.content = ViewList("",'c')

    def extract(self, source):
        """
        Process the source file and fill in the content.
        SOURCE is a fileobject.
        """
        for l in source:
            l = l.strip()
            m = re_comment.match(l)
            if m:
                self.comment(m.group(1), source)
        
    
    def comment(self, cur, source):
        """
        Read the whole comment and strip the stars.
        CUR is currently read line and SOURCE is a fileobject with the source code.
        """
        cmt = ""
        m = re_cmtend.match(cur)
        if m:
            cmt = cmt +  m.group(0)
        else:
            cmt = cmt +  cur

        for cur in source:
            cur = cur.strip()
            if cur == '':
                continue

            if cur.startswith("/*"):
                raise ExtractError("Nested comments are not supported yet.")

            if re_cmtend.match(cur):
                break
            
            m = re_cmtnext.match(cur)
            if m:
                print(m.group(1))
                cmt  = cmt + m.group(1)
            
        self.content.append(cmt, "c")


    def printrst(self):
        """
        Print the sphinx rst to stdout.
        """
        print(self.content)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: extractor.py <file.c|cpp|h>")
        exit(1)

    extractor = Extractor()
    try:
        with open(sys.argv[1], 'r') as f:
            extractor.extract(f)
    except ExtractError as e:
        print('Extraction error in external source file %r : %s'
                    % (sys.argv[1], str(e)))
    extractor.printrst()
    

    
