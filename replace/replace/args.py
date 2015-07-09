#/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-05-19 14:03:37
# Filename      : args.py
# Description   : 
import optparse
from replace import version
import os

def parser_args():
    usage = "Usage: %prog [options] target_path"

    parser = optparse.OptionParser(usage, 
            version = version)


    _help = "exclude files matching PATTERN"
    parser.add_option('--filter_filename',
            dest = 'filter_filename', type = str, action="append",
            metavar = 'PATTERN', help = _help)

    _help = 'only include files matching PATTERN(high priority)'
    parser.add_option('--include_filename', 
            dest = 'include_filename', type = str, action="append",
            metavar = 'PATTERN', help = _help)

    _help = 'source re pattern'
    parser.add_option('-s', '--source', type = str,
            dest = 'source_re_string', help = _help)

    _help = 'target string'
    parser.add_option('-t', '--target', type = str,
            dest = 'target_string', help = _help)

    _help = 'include hidden file'
    parser.add_option('-H', default = False, action = "store_true", dest="include_hidden", help = _help)

    opt, args = parser.parse_args()

    if opt.source_re_string == None or opt.target_string == None:
        parser.error('--source or --target be must')

    for target_path in args:
        if not os.path.exists(target_path):
            parser.error("%s is not exists" % (target_path, ))

    return opt, args

