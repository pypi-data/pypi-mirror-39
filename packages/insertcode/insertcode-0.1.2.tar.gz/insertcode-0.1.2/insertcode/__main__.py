#! /usr/bin/env python

import extargsparse
import sys
import os
import logging
import re
import bz2
import base64

def set_log_level(args):
    loglvl= logging.ERROR
    if args.verbose >= 3:
        loglvl = logging.DEBUG
    elif args.verbose >= 2:
        loglvl = logging.INFO
    elif args.verbose >= 1 :
        loglvl = logging.WARN
    # we delete old handlers ,and set new handler
    if logging.root is not None and logging.root.handlers is not None and len(logging.root.handlers) > 0:
        logging.root.handlers = []
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    return

def __get_bash_string_file(infile):
    s = ''
    logging.info('open file [%s] for string'%(infile))
    with open(infile,'rb')  as fin:
        for l in fin:
            if sys.version[0] == '3' and 'b' in fin.mode:
                l = l.decode('utf-8')
            curs = ''
            for c in l:
                if c == '$':
                    curs += '\\'
                    curs += '$'
                elif c == '\\':
                    curs += '\\\\'
                elif c == '`':
                    curs += '\\'
                    curs += '`'
                else:
                    curs += c
            s += curs
            logging.info('[%s] => [%s]'%(l,curs))
    #logging.info('[%s] (%s)'%(infile,s))
    return s

def get_bash_string(args):
    s = ''
    for c in args.subnargs:
        s += __get_bash_string_file(c)
    return s

def replace_string(args,repls):
    fin = sys.stdin
    fout = sys.stdout
    if args.input is not None:
        fin = open(args.input,'rb')
    if args.output is not None:
        fout = open(args.output,'w+b')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        chgstr = l.replace(args.pattern,repls)
        if sys.version[0] == '3' and 'b' in fout.mode:
            fout.write(chgstr.encode('utf-8'))
        else:
            fout.write('%s'%(chgstr))
    if fin != sys.stdin:
        fin.close()
    fin = None
    if fout != sys.stdout:
        fout.close()
    fout = None
    return

def out_string(args,repls):
    fout = sys.stdout
    if args.output is not None:
        fout = open(args.output,'w+b')

    fout.write('%s'%(repls))

    if fout != sys.stdout:
        fout.close()
    fout = None
    return

def __get_insert_string_file(infile):
    s = ''
    i = 0
    logging.info('open [%s] for insert string'%(infile))
    with open(infile,'rb') as fin:
        i = 0
        for l in fin:
            if sys.version[0] == '3' and 'b' in fin.mode:
                l = l.decode('utf-8')
            i += 1
            if i == 1 and l.startswith('#!'):
                continue
            s += l
    logging.info('[%s] (%s)'%(infile,s))
    return s

def get_insert_string(args):
    s = ''
    for f in args.subnargs:
        s += __get_insert_string_file(f)
    return s

def bashinsert_handler(args,parser):
    set_log_level(args)
    repls = get_insert_string(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def bashstring_handler(args,parser):
    set_log_level(args)
    repls = get_bash_string(args)
    replace_string(args,repls)
    sys.exit(0)
    return





def __get_make_python(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '\r':
                s += '\\\\'
                s += 'r'
            elif c == '\n':
                s += '\\\\'
                s += 'n'
            elif c == '\t':
                s += '\\\\'
                s += 't'
            elif c == '\\':
                s += '\\\\\\\\'
            elif c == '\'':
                s += '\\\\\''
            elif c == '"':
                s += '\\"'
            elif c == '$':
                s += '\\$$'
            elif c == '`':
                s += '\\'
                s += '`'
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s


def get_make_python(args):
    s = ''
    for infile in args.subnargs:
        s += __get_make_python(args,infile)
    return s

def makepython_handler(args,parser):
    set_log_level(args)
    repls = get_make_python(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def __get_make_perl(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '#':
                s += '\\'
                s += '#'
            elif c == '\n':
                s += '\\'
                s += 'n'
            elif c == '$':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '$'
                s += '$'
            elif c == '"':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '"'
            elif c == '\\':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '\\'
            elif c == '`':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '`'
            elif c == '\r':
                s += '\\'
                s += 'r'
            elif c == '\t':
                s += '\\'
                s += 't'
            elif c == '@':
                s += '\\'
                s += '@'
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def get_make_perl(args):
    s = ''
    for infile in args.subnargs:
        s += __get_make_perl(args,infile)
    return s

def makeperl_handler(args,parser):
    set_log_level(args)
    repls = get_make_perl(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def __get_sh_perl(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '#':
                s += '\\'
                s += '#'
            elif c == '\n':
                s += '\\'
                s += 'n'
            elif c == '$':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '$'
            elif c == '"':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '"'
            elif c == '\\':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '\\'
            elif c == '`':
                s += '\\'
                s += '`'
            elif c == '\r':
                s += '\\'
                s += 'r'
            elif c == '\t':
                s += '\\'
                s += 't'
            elif c == '@':
                s += '\\'
                s += '@'
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def get_sh_perl(args):
    s = ''
    for infile in args.subnargs:
        s += __get_sh_perl(args,infile)
    return s

def shperl_handler(args,parser):
    set_log_level(args)
    repls = get_sh_perl(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def __get_sh_python(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '\n':
                s += '\\'
                s += 'n'
            elif c == '$':
                s += '\\'
                s += '$'
            elif c == '"':
                s += '\\'
                s += '"'
            elif c == '\\':
                s += '\\'
                s += '\\'
                s += '\\'
                s += '\\'
            elif c == '`':
                s += '\\'
                s += '`'
            elif c == '\r':
                s += '\\'
                s += 'r'
            elif c == '\t':
                s += '\\'
                s += 't'
            elif c == '\'':
                s += '\\\\'
                s += '\''
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def get_sh_python(args):
    s = ''
    for infile in args.subnargs:
        s += __get_sh_python(args,infile)
    return s

def shpython_handler(args,parser):
    set_log_level(args)
    repls = get_sh_python(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def __get_python_perl(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '\n':
                s += '\\'
                s += '\\'
                s += 'n'
            elif c == '#':
                s += '\\'
                s += '\\'
                s += '#'
            elif c == '$':
                s += '\\' * 6
                s += '$'
            elif c == '"':
                s += '\\' * 6
                s += '"'
            elif c == '\\':
                s += '\\' * 8
            elif c == '\'':
                s += '\\'
                s += '\''
            elif c == '@':
                s += '\\' * 2
                s += '@'
            elif c == '`':
                s += '\\' * 2
                s += '`'
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def get_python_perl(args):
    s = ''
    for infile in args.subnargs:
        s += __get_python_perl(args,infile)
    return s

def pythonperl_handler(args,parser):
    set_log_level(args)
    repls = get_python_perl(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def __get_python_c(args,infile):
    s = ''
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')

    for l in fin:
        if sys.version[0] == '3' and 'b' in fin.mode:
            l = l.decode('utf-8')
        for c in l:
            if c == '\'':
                s += '\\'
                s += '\''
            elif c == '\\':
                s += '\\'
                s += '\\'
            else:
                s += c
    if fin != sys.stdin:
        fin.close()
    fin = None
    return s

def get_python_c(args):
    s = ''
    for infile in args.subnargs:
        s += __get_python_c(args,infile)
    return s

def pythonc_handler(args,parser):
    set_log_level(args)
    repls = get_python_c(args)
    replace_string(args,repls)
    sys.exit(0)
    return

def version_handler(args,parser):
    sys.stdout.write('insertcode 0.1.2\n')
    sys.exit(0)
    return

def __get_bz2_base64(args,infile):
    fin = open(infile,'rb')
    data = fin.read()
    if 'b' not in fin.mode:
        if sys.version[0] == '3':
            data = data.encode('utf-8')
        else:
            data = bytes(data)
    fin.close()
    fin = None
    cmprdata = bz2.compress(data,9)
    retdata = base64.b64encode(cmprdata)
    if sys.version[0] == '3':
        retdata = retdata.decode('utf-8')
    else:
        retdata = str(retdata)
    return retdata

def get_bz2_base64(args):
    s = ''
    for f in args.subnargs:
        s += __get_bz2_base64(args,f)
    return s

def bz2base64_handler(args,parser):
    set_log_level(args)
    repls = get_bz2_base64(args)
    replace_string(args,repls)
    sys.exit(0)
    return

GL_ECHO_BASE64_STR='''
import bz2
import base64
import sys
GL_REPLACE_STRING=\'\'\'%REPLACE_PATTERN%\'\'\'
code = base64.b64decode(GL_REPLACE_STRING)
s = bz2.decompress(code)
if sys.version[0] == '3':
    s = s.decode('utf-8')
sys.stdout.write('%s'%(s))
'''

def bz2base64mak_handler(args,parser):
    set_log_level(args)
    s = get_bz2_base64(args)
    ins = ''
    ins = GL_ECHO_BASE64_STR.replace('%REPLACE_PATTERN%', s)
    s = ''
    for c in ins:
        if c == '\r':
            s += '\\\\'
            s += 'r'
        elif c == '\n':
            s += '\\\\'
            s += 'n'
        elif c == '\t':
            s += '\\\\'
            s += 't'
        elif c == '\\':
            s += '\\\\\\\\'
        elif c == '\'':
            s += '\\\\\''
        elif c == '"':
            s += '\\"'
        elif c == '$':
            s += '\\$$'
        elif c == '`':
            s += '\\'
            s += '`'
        else:
            s += c
    replace_string(args,s)
    sys.exit(0)
    return

def main():
    commandline='''
    {
        "verbose|v" : "+",
        "input|i##default (stdin)##" : null,
        "output|o##default (stdout)##": null,
        "pattern|p" : "%REPLACE_PATTERN%",
        "bashinsert<bashinsert_handler>" : {
            "$" : "*"
        },
        "bashstring<bashstring_handler>" : {
            "$" : "*"
        },
        "makepython<makepython_handler>" : {
            "$" : "*"
        },
        "makeperl<makeperl_handler>" : {
            "$" : "*"
        },
        "shperl<shperl_handler>" : {
            "$" : "*"
        },
        "shpython<shpython_handler>" : {
            "$" : "*"
        },
        "pythonperl<pythonperl_handler>" : {
            "$" : "*"
        },
        "pythonc<pythonc_handler>" : {
            "$" : "*"
        },
        "version<version_handler>" : {
            "$" : 0
        },
        "bz2base64<bz2base64_handler>" : {
            "$" : 1
        },
        "bz2base64mak<bz2base64mak_handler>" : {
            "$" : 1
        }
    }
    '''
    options = extargsparse.ExtArgsOptions('{ "version" : "0.1.2"}')
    parser = extargsparse.ExtArgsParse()
    parser.load_command_line_string(commandline)
    args = parser.parse_command_line(None,parser)
    sys.stderr.write('no handler specified')
    sys.exit(4)
    return


if __name__ == '__main__':
    main()
