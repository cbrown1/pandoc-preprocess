# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 17:16:55 2016

@author: cbrown
"""

import datetime
import re
import argparse
import fileinput

class question_orders():
    """Simple pandoc preprocessor script to perform variable expansion using 
        data pulled from a text file. 
        Given a string and a datafile, finds all occurrences of the format
        '[[3]]' with the text from the corresponding line number in the datafile.
        
        Parameters
        ----------
        
        source : str
            The text of the source, either a file or stdin. Variable format is
            a number surrounded by double brackets like this: [[2]], which will
            be replaced by the text from the specified line in the datafile.
        data : str
            A text datafile to use. Each bit of text should be on its own line.

        Returns
        -------
        
        processed : str
            The source text, with variables expanded as described.
            
    """

    pattern = re.compile(r"\[\[([0-9]+)\]\]")

    def process(self, source, data1, data2):

        matches = self.pattern.findall(source)
        for match in matches:
#            print "Match: {}".format(match)
            num = data1[int(match)-1]
#            print "num: {}".format(num)
            new = data2.index(num)
#            print "New: {}".format(new)
            print match, num, str(new+1)
            source = source.replace("[[{}]]".format(match), str(new+1))
        return source


if __name__ == "__main__":

    desc = """Simple pandoc preprocessor script to perform variable expansion using 
            data pulled from a text file. 
            Given a string and a datafile, finds all occurrences of the format
            '[[3]]' with the text from the corresponding line number in the datafile.
            """
    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument("source_file", type=str,
                        help="The path to the source md file, or - for stdin")
    parser.add_argument("-x", "--order1", default=None, type=str,
                        help="The path to data file 1 to use.")
    parser.add_argument("-y", "--order2", default=None, type=str,
                        help="The path to data file 2 to use.")
    parser.add_argument("-o", "--output", default=None, type=str,
                        help="the path to the output md file. If ommitted, write to stdout")

    args = parser.parse_args()
    preproc = question_orders()

    preproc.source = args.source_file
    datafile1 = args.order1
    datafile2 = args.order2
    out_file = args.output

    source = ""
    for line in fileinput.input(preproc.source):
        source += line

    data1 = []
    for line in fileinput.input(datafile1):
        data1.append(line.strip())
    data2 = []
    for line in fileinput.input(datafile2):
        data2.append(line.strip())

    new_data = preproc.process( source, data1, data2 )

    if out_file:
        with open(out_file, 'w') as h:
            h.write(new_data)
    else:
        sys.stdout.write(new_data)
