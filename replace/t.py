#coding:utf-8
from __future__ import unicode_literals, print_function

from replace.core import FilesManager
from replace.args import parser_args


def replace(options, target_path=None):
    filter_filename = options.include_filename or options.filter_filename
    is_filter = not bool(options.include_filename)
    files_manager = FilesManager(target_path, filter_filename = filter_filename,
            is_filter = is_filter,
            source_re_string = options.source_re_string,
            target_string = options.target_string,
            include_hidden = options.include_hidden)

    for _file in files_manager.list_all_files():
    #    print(_file)
        pass
    # files_manager.all_replace()

if __name__ == "__main__":
    options, target_path_list = parser_args()
    for target_path in target_path_list or [None]:
        replace(options, target_path)

