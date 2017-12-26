# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 17:16:55 2016

@author: cbrown
"""

import datetime
import re
import argparse
import fileinput

class syllabus_dates():
    """Given a string and a year, finds all occurrences of the format
        '[[W02-D2]]' with their respective dates. 'W02' should be the week
        of the year, and 'D2' should be the day of the week; 1==Mon.

        This may be useful in updating syllabi schedules, where the days of the
        week and the weeks of the year don't change (eg., Classes are Tue, Thu;
        exam 1 is always on Thursday of the 3rd week of the semester), but the  
        actual dates do from year to year.
        
        Parameters
        ----------
        
        syllabus : str
            The text of the syllabus
        year : str
            The year in which to create the dates in the syllabus
        date : str
            A datetime formatting string with which to format the resulting
            dates. Default = "%a, %b %d"

        Returns
        -------
        
        syllabus : str
            The syllabus text, with formatted dates
            
    """

    pattern = re.compile(r"\[\[([A-Za-z0-9_\-]+)\]\]")

    date_fmt = "%a, %b %d"

    def process(self, syllabus, year):

        matches = self.pattern.findall(syllabus)
        for match in matches:
            d = "{}-{}".format(year,match)
            d1 = datetime.datetime.strptime(d, "%Y-W%W-D%w")
            syllabus = syllabus.replace("[[{}]]".format(match), d1.strftime(self.date_fmt))
        return syllabus


if __name__ == "__main__":

    desc = """Simple pandoc preprocessor script to process syllable dates. 
            Given a string and a year, finds all occurrences of the format
            '[[W02-D2]]' with their respective dates. 'W02' should be the week
            of the year, and 'D2' should be the day of the week; 1==Mon.
            
            This may be useful in updating syllabi schedules, where the days of the
            week and the weeks of the year don't change (eg., Classes are Tue, Thu;
            exam 1 is always on Thursday of the 3rd week of the semester), but the  
            actual dates do from year to year.
            """

    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument("source_file", type=str,
                        help="The path to the source md file, or - for stdin")
    parser.add_argument("-y", "--year", default=None, type=str,
                        help="The year to use to process dates.")
    parser.add_argument("-d", "--date_format", default=None, type=str,
                        help="The datetime format to use. Default is '%%a, %%b %%d' -> 'Tue, Mar 02'")
    parser.add_argument("-o", "--output", default=None, type=str,
                        help="the path to the output md file. If ommitted, write to stdout")

    args = parser.parse_args()
    preproc = syllabus_dates()

    preproc.source = args.source_file
    year = args.year
    if args.date_format:
        preproc.date_fmt = args.date_format
    out_file = args.output

    data = ""
    for line in fileinput.input(preproc.source):
        data += line

    new_data = preproc.process( data, year )

    if out_file:
        with open(out_file, 'w') as h:
            h.write(new_data)
    else:
        sys.stdout.write(new_data)
