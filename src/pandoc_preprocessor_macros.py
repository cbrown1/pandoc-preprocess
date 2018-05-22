#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import csv
import yaml
from yamlreader import data_merge
import argparse
import fileinput
import daiquiri

def read_yaml_header(raw):
    # Read in file. Take first section as yml block, everything else as body
    preamble = raw.split('---')[1]
    if raw.find('---') == -1:
        body = ""
    else:
        body = raw.split('---')[2]
    return preamble, body

class preproc_macros():
    """ Allows macro processing in markdown. Useful as a pandoc preprocessor.

        Variables can be set in the macro, in the yaml header, or at the command line.

        There are two types of variables. vars are expanded typically.
        idvars are expanded using an id as the key into a dict, to allow different values
        to be inserted based on the id. idvars cannot be set in the macro, but this isn't 
        needed since the id is known at that level.
        
        To use, specify macros in your markdown like this:
    
            ![:macro_name var1=val2](id)
    
    """

    proc = {}
    variables = {}
    idvariables = {}
    re_macro_string = '\!\[\:macro[ ]?(.*?)\]\([\"\']{0,1}(.*?)[\"\']{0,1}\)'

    daiquiri.setup(level=5)
    logger = daiquiri.getLogger(__name__)
    debug = False

    def proc_var_old(self, var):
        if os.path.isfile(var):
            val = open(var, 'r').read()
            return val, 'file'
        else:
            return var, 'str'

    def proc_var(self, store, key, val, valtype, vartype):
        if val.startswith('file://') and  os.path.isfile(val[7:]):
            thisval = open(val[7:], 'r').read()
            fmt = 'file'
            shortval = self.truncate(val[7:], pre=True)
        else:
            thisval = val
            fmt = 'str'
            shortval = self.truncate(val)
        store[ key ] = thisval
        if self.debug:
            self.logger.debug('Found {fmt} {valtype}: {key}; source: {vartype}; val: {val}'.format(
                fmt=fmt, valtype=valtype, val=shortval, key=key, vartype=vartype))

        return store

    def truncate(self, var, pre=False, n=20):
        val = var.replace(os.linesep, " ")
        if pre:
            val = '...' + val[3:] if len(val) > n else val
        else:
            val = val[:n-3] + '...' if len(val) > n else val
        return val

    def init_vars_metadata ( self, metadata ):

        if metadata.has_key('macro_vars'):
            for item in metadata['macro_vars']:
                if isinstance(item, str):
                    for key,val in metadata[item].iteritems():
                        self.proc_var(self.variables, key, val, "var", "metadata variable")
                else:
                    for key,val in item.iteritems():
                        self.proc_var(self.variables, key, val, "var", "metadata dict")

        if metadata.has_key('macro_idvars'):
            for item in metadata['macro_idvars']:
                for key,val in metadata[item].iteritems():
                    outkey = item + "||" + key
                    self.proc_var(self.idvariables, outkey, val, "idvar", "metadata variable")

        if metadata.has_key('macro_proc'):
            for key,val in metadata['macro_proc'].iteritems():# For each item:
                if os.path.isfile(val):                       # If the val is a real file:
                    self.proc [key] = open(val, 'r').read()   #   Read contents as template
                    self.logger.debug('Found macro name: {} and file template: {} in macro_proc metadata variable'.format(key, self.truncate(val, pre=True)))
                else:                                         # Otherwise:
                    self.proc [key] = metadata[val]           #   Assume metadata var is template
                    self.logger.debug('Found macro name: {} and metadata str template: {} in macro_proc metadata variable'.format(key, self.truncate(val)))


    def init_vars_args( self, args ):

        if args.var:
            for v in args.var:
                items = v.split(",")
                for item in items:
                    if ":" in item:
                        key,val = item.split(":")
                        self.proc_var(self.variables, key, val, "var", "command line")
                    else:
                        for key,val in metadata[item].iteritems():
                            self.proc_var(self.variables, key, val, "var", "metadata variable from command line")

        if args.idvar:
            for v in args.idvar:
                items = v.split(",")
                for item in items:
                    if "(" in item:
                        key,idval = item.split("(")
                        if not self.idvariables.has_key(key):
                            self.idvariables[key] = {}
                        id,val = idval.split(":")
                        val = val.strip(")")
                        outkey = id + "||" + key
                        self.proc_var(self.idvariables, outkey, val, "idvar", "command line")
                    else:
                        for key,val in metadata[item].iteritems():
                            outkey = item + "||" + key
                            self.proc_var(self.idvariables, key, val, "idvar", "metadata variable from command line")

        if args.proc:
            items = args.proc.split(",")
            for item in items:
                key,val = item.split(":")
                if os.path.isfile(val):                       # If the val is a real file:
                    self.proc [key] = open(val, 'r').read()   #   Read contents as template
                    self.logger.debug('Found filepath template: {} and macro name: {} in proc command line variable'.format(self.truncate(val), key))
                else:                                         # Otherwise:
                    self.proc [key] = metadata[val]           #   Assume metadata var is template
                    self.logger.debug('Found str template: {} and macro name: {} in proc command line variable'.format(self.truncate(val), key))
            # TODO: template arg was just added to argparser and are not properly parsed here. template -> arg.template, etc.
            if os.path.isfile(template):
                self.proc[name] = open(template, 'r').read()
                self.logger.debug('Found file template from command line: {}'.format(template))
            else:
                self.proc[name] = metadata[template]
                self.logger.debug('Found str template metadata str from command line: {}'.format(template))

    def process ( self, data ):

        for name,template in self.proc.iteritems():

            re_macro_string = str(self.re_macro_string)
            re_macro_string = re_macro_string.replace('macro', name)
            re_macro = re.compile(re_macro_string)

            for m in re_macro.finditer(data):

                lineno = data.count(os.linesep,0,m.start())+1

                self.logger.debug("Processing macro {}".format(m.group(0)))

                # Get new vars
                t = str(template)
                variables = dict(self.variables)

                # Extract vals from input text block
                id = m.group(2).strip(" \"\'")
                variables['id'] = id
                for line in csv.reader([m.group(1)], quotechar='"', delimiter=',', skipinitialspace=True):
                    for v in line:
                        key,val = v.split("=")
                        key = key.strip(" \"\'")
                        val = val.strip(" \"\'")
                        #print(os.path.isfile(val))
                        #variables[var] = val
                        variables = self.proc_var(variables, key, val, "var", "macro variable")

                # Process idvars first, since id will be expanded when vars are processed
                for var,val in self.idvariables.iteritems():
                    varvar,varid = var.split("||")
                    if id == varid:
                        if t.find("$id({})".format(varvar)) != -1:
                            self.logger.debug("  Processing id: {}; idvar: {}; val: {}".format(varid, varvar, self.truncate(val)))
                            t = t.replace("$id({})".format(varvar), val)

                # Insert vals into output text block
                for var,val in variables.iteritems():
                    if t.find(var) != -1:
                        self.logger.debug("  Processing var: {}; val: {}".format(var, self.truncate(val)))
                        t = t.replace("${}".format(var), val)
            
                # Insert output text block into output text
                data = data.replace(m.group(0), t)
            
        return data
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Simple pandoc preprocessor script to process macros")
    parser.add_argument("-o", "--output", default=None, type=str,
                        help="the path to the output md file. If ommitted, write to stdout")
    parser.add_argument("-d", "--debug", default=False, action='store_true',
                        help="Include switch to enable debugging output. Default = no debugging")
    parser.add_argument("-p", "--proc", default=None, type=str,
                        help="A comma-separated list of name:template pairs to process. The name is the macro name to search for, the template is either the path to a file, or the name of a yaml metadata variable, containing the the template text to use.")
    parser.add_argument("-t", "--template", default=None, type=str,
                        help="A file or string specifying a template.")
    parser.add_argument("-v", "--var", default=None, type=str, action='append',
                        help="A comma-separated list of variables needed. If an item is delimited with a colon (key:val), then it will be added to the variable list. in the form key1:val1,key2:val2")
    parser.add_argument("-i", "--idvar", default=None, type=str, action='append',
                        help="A comma-separated list of variables to be expanded by id. To specify idvars at the command line, use the form var1(id1:val1),var1(id2:val2). Think of figure captions: caption(fig1:This is the caption). To specify a yaml header variable, just name it: var1. The yaml variable should be a dict with ids as keys. The id is the main parameter in the macro (in parentheses). Specify an idvar in your template with $id(var1). For the caption example, $id(caption)")
    parser.add_argument("source_files", nargs='+', type=str,
                        help="the path to the source md file or files, or - for stdin") # Returns a list
    args = parser.parse_args()

    out_file = args.output
    source_files = args.source_files

    preproc = preproc_macros()

    preproc.debug = args.debug

    meta = {}
    body = ""
    for source_file in source_files:
        raw = ""
        # Read in md file as str
        for line in fileinput.input(source_file):
            raw += line

        # Split into head (yaml) and body (md)
        this_head,this_body = read_yaml_header(raw)
        # Load yaml str into metadata dict
        this_meta = yaml.safe_load(this_head)
        # Merge this metadata dict with others (function imported from pypi package yamlreader)
        meta = data_merge(meta, this_meta)
        # Merge this body str with others
        body = body + this_body

    preproc.init_vars_metadata(meta)
    preproc.init_vars_args(args)

    new_body = preproc.process( body )

    delim = "---" + os.linesep
    # Create new file. The metadata here is ugly but usable
    new_file = delim + yaml.safe_dump(meta) + delim + new_body

    if out_file:
        with open(out_file, "w") as f:
            f.write(new_file)
            f.flush()
    else:
        print(new_file)
