#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import argparse
import fileinput

class critic():
    
    source = None
    re_substitution = re.compile('{\~\~(.*?)~>(.*?)\~\~}')
    re_addition = re.compile('{\+\+(.*?)\+\+}')
    re_deletion = re.compile('{\-\-(.*?)\-\-}')
    re_highlight = re.compile('{\=\=(.*?)\=\=}')
    re_comment = re.compile('{\>\>(.*?)\<\<}')
    re_comment_attribution = re.compile('^\@(\S*)')
    
    class addition():
        orig = ""
        val = ""
        start = None
        end = None
        line = None
    
    class deletion():
        orig = ""
        val = ""
        start = None
        end = None
        line = None
    
    class substitution():
        orig = ""
        val = ""
        old = ""
        start = None
        end = None
        line = None
    
    class highlight():
        orig = ""
        val = ""
        start = None
        end = None
        line = None
    
    class comment():
        orig = ""
        val = ""
        start = None
        end = None
        author = None
        line = None
    
    comments = []
    additions = []
    deletions = []
    substitutions = []
    highlights = []
    
    show_highlights = False
    show_comments = False
    
    format_substitution = None
    format_addition = None
    format_comment = None
    format_highlight = None

    format_var = "@str"
    
    def process(self, data, proc='show'):
    
        if proc == 'show': 
            if self.format_addition != '-1':
                for addition in self.additions:
                    if self.format_addition:
                        val = self.format_addition.replace(self.format_var, addition.val)
                    else:
                        val = addition.val
                    data = data.replace(addition.orig, val)

            if self.format_deletion != '-1':
                for deletion in self.deletions:
                    if self.format_deletion:
                        val = self.format_deletion.replace(self.format_var, deletion.val)
                    else:
                        val = ""
                    data = data.replace(deletion.orig, val)

            if self.format_substitution != '-1':
                for substitution in self.substitutions:
                    if self.format_substitution:
                        val = self.format_substitution.replace(self.format_var, substitution.val)
                    else:
                        val = substitution.val
                    data = data.replace(substitution.orig, val)
    
            if self.format_highlight != '-1':
                for highlight in self.highlights:
                    if self.format_highlight:
                        val = self.format_highlight.replace(self.format_var, highlight.val)
                    else:
                        val = highlight.val
                    data = data.replace(highlight.orig, val)

            if self.format_comment != '-1':
                for comment in self.comments:
                    # TODO: Consider adding facility to formatter to handle the author
                    if self.format_comment:
                        val = self.format_comment.replace(self.format_var, comment.val)
                    else:
                        val = ""
                    data = data.replace(comment.orig, val)

            return data

        elif proc == 'hide': 
            for addition in self.additions:
                data = data.replace(addition.orig, "")
            for deletion in self.deletions:
                data = data.replace(deletion.orig, deletion.val)
            for substitution in self.substitutions:
                data = data.replace(substitution.orig, substitution.old)
            for highlight in self.highlights:
                data = data.replace(highlight.orig, highlight.val)
            for comment in self.comments:
                data = data.replace(comment.orig, "")
        
            return data

        elif proc == 'list':
            s = os.linesep
            out = "source: '{}'{}".format(self.source,s)
            out += "{}".format(s)

            if len(self.additions) == 0:
                out += "additions: None{}".format(s)
                out += "{}".format(s)
            else:
                out += "additions:{}".format(s)
                for addition in self.additions:
                    out += "    - start: {}{}".format(addition.start,s)
                    out += "      end: {}{}".format(addition.end,s)
                    out += "      line: {}{}".format(addition.line,s)
                    out += "      original: |-4{}".format(s)
                    out += "          {}{}".format(addition.orig,s)
                    out += "      value: |-4{}".format(s)
                    out += "          {}{}".format(addition.val,s)
                    out += "{}".format(s)

            if len(self.deletions) == 0:
                out += "deletions: None{}".format(s)
                out += "{}".format(s)
            else:
                out += "deletions:{}".format(s)
                for deletion in self.deletions:
                    out += "    - start: {}{}".format(deletion.start,s)
                    out += "      end: {}{}".format(deletion.end,s)
                    out += "      line: {}{}".format(deletion.line,s)
                    out += "      original: |-4{}".format(s)
                    out += "          {}{}".format(deletion.orig,s)
                    out += "      value: |-4{}".format(s)
                    out += "          {}{}".format(deletion.val,s)
                    out += "{}".format(s)

            if len(self.additions) == 0:
                out += "substitutions: None{}".format(s)
                out += ""
            else:
                out += "substitutions:{}".format(s)
                for substitution in self.substitutions:
                    out += "    - start: {}{}".format(substitution.start,s)
                    out += "      end: {}{}".format(substitution.end,s)
                    out += "      line: {}{}".format(substitution.line,s)
                    out += "      original: |-4{}".format(s)
                    out += "          {}{}".format(substitution.orig,s)
                    out += "      old: |-4{}".format(s)
                    out += "          {}{}".format(substitution.old,s)
                    out += "      value: |-4{}".format(s)
                    out += "          {}{}".format(substitution.val,s)
                    out += "{}".format(s)

            if len(self.highlights) == 0:
                out += "highlights: None{}".format(s)
                out += "{}".format(s)
            else:
                out += "highlights:{}".format(s)
                for highlight in self.highlights:
                    out += "    - start: {}{}".format(highlight.start,s)
                    out += "      end: {}{}".format(highlight.end,s)
                    out += "      line: {}{}".format(highlight.line,s)
                    out += "      original: |-4{}".format(s)
                    out += "          {}{}".format(highlight.orig,s)
                    out += "      value: |-4{}".format(s)
                    out += "          {}{}".format(highlight.val,s)
                    out += "{}".format(s)

            if len(self.comments) == 0:
                out += "comments: None{}".format(s)
                out += "{}"
            else:
                out += "comments:{}".format(s)
                for comment in self.comments:
                    out += "    - start: {}{}".format(comment.start,s)
                    out += "      end: {}{}".format(comment.end,s)
                    out += "      line: {}{}".format(comment.line,s)
                    out += "      original: |-4{}".format(s)
                    out += "          {}{}".format(comment.orig,s)
                    out += "      value: |-4{}".format(s)
                    out += "          {}{}".format(comment.val,s)
                    if comment.author:
                        out += "      author: |-4{}".format(s)
                        out += "          {}{}".format(comment.author,s)
                    out += "{}".format(s)

            return out


    def find(self, data):
        
        s = "\n" # Just use \n, since it will be found regardless of os

        for m in self.re_addition.finditer(data):
            this = self.addition()
            this.start = m.start(0)
            this.end = m.end(0)
            this.line = data.count(s,0,this.start) + 1
            this.orig = m.group(0)
            this.val = m.group(1)
            self.additions.append(this)
            
        for m in self.re_deletion.finditer(data):
            this = self.deletion()
            this.start = m.start(0)
            this.end = m.end(0)
            this.line = data.count(s,0,this.start) + 1
            this.orig = m.group(0)
            this.val = m.group(1)
            self.deletions.append(this)
            
        for m in self.re_substitution.finditer(data):
            this = self.substitution()
            this.start = m.start(0)
            this.end = m.end(0)
            this.line = data.count(s,0,this.start) + 1
            this.orig = m.group(0)
            this.old = m.group(1)
            this.val = m.group(2)
            self.substitutions.append(this)
            
        for m in self.re_highlight.finditer(data):
            this = self.highlight()
            this.start = m.start(0)
            this.end = m.end(0)
            this.line = data.count(s,0,this.start) + 1
            this.orig = m.group(0)
            this.val = m.group(1)
            self.highlights.append(this)
            
        for m in self.re_comment.finditer(data):
            this = self.comment()
            if m.group(1).strip().startswith("@"):
                ma = self.re_comment_attribution.match(m.group(1))
                this.author = ma.group(0)
                this.val = m.group(1).replace(this.author, "").strip()
            else:
                this.val = m.group(1).strip()
            this.start = m.start(0)
            this.end = m.end(0)
            this.line = data.count(s,0,this.start) + 1
            this.orig = m.group(0)
            self.comments.append(this)


if __name__ == "__main__":

    desc = """Simple pandoc preprocessor script to process criticmarkup edits. 
           """

    procstr = """How to process the changes. 
                   'show' will show changes [default], formatted if specified.
                   'hide' will remove changes and revert to the original text.
                   'list' will print the changes to the specified output, in yaml format.
    """

    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument("source_file", type=str,
                        help="The path to the source md file, or - for stdin")
    parser.add_argument("-o", "--output", default=None,
                        help="The path to the output file, or stdout if omitted.")
    parser.add_argument("-p", "--process", default=None, type=str,
                        help=procstr)
    parser.add_argument("-a", "--addition", default=None, type=str,
                        help="How to process additions, only used when proc=show. Omit for no formatting, -1 to skip processing additions, or a format string. Use &str for the text. EG., \\textcolor{green}{@str}")
    parser.add_argument("-d", "--deletion", default=None, type=str,
                        help="How to process deletions, only used when proc=show. Omit for no formatting, -1 to skip processing deletions, or a format string. Use &str for the text. EG., \\textcolor{red}{@str}")
    parser.add_argument("-s", "--substitution", default=None, type=str,
                        help="How to process substitutions, only used when proc=show. Omit for no formatting, -1 to skip processing substitutions, or a format string. Use &str for the text. EG., \\textcolor{orange}{@str}")
    parser.add_argument("-l", "--highlight", default=None, type=str,
                        help="How to process highlights, only used when proc=show. Omit for no formatting, -1 to skip processing highlights, or a format string. Use &str for the text. EG., \\textcolor{yellow}{@str}")
    parser.add_argument("-c", "--comment", default=None, type=str,
                        help="How to process comments, only used when proc=show. Omit for no formatting, -1 to skip processing comments, or a format string. Use &str for the text. EG., \\textcolor{blue}{@str}")
    parser.add_argument("-f", "--format_string", default=None, type=str,
                        help="The variable to search for in format strings to be replaced by text. Default is @str. EG., \\textcolor{red}{@str}")
    args = parser.parse_args()

    preproc = critic()

    preproc.source = args.source_file
    preproc.dest = args.output

    if args.format_string: 
        preproc.format_string = args.format_string
    if args.process:
        proc = args.process
    else:
        proc = 'show'
    preproc.format_addition = args.addition
    preproc.format_deletion = args.deletion
    preproc.format_comment = args.comment
    preproc.format_highlight = args.highlight
    preproc.format_substitution = args.substitution

    data = ""
    for line in fileinput.input(preproc.source):
        data += line

    preproc.find(data)
    new_data = preproc.process(data, proc)

    if preproc.dest:
        with open(preproc.dest, 'w') as h:
            h.write(new_data)
    else:
        sys.stdout.write(new_data)

       
#    print("{:} additions".format(len(preproc.additions)))
#    print("{:} deletions".format(len(preproc.deletions)))
#    print("{:} substitutions".format(len(preproc.substitutions)))
#    print("{:} highlights".format(len(preproc.highlights)))
#    print("{:} comments".format(len(preproc.comments)))
#    for c in preproc.comments:
#        print("  {}: {}".format(c.author, c.val))
