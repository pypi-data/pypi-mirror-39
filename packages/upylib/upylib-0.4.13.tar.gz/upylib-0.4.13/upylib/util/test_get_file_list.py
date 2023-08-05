#!/usr/bin/env python
# -*- coding:utf-8 -*-⏎

from __future__ import print_function
from fs import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def test():
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
    print( "test invlid")
    file_list = get_file_list("a")

    print( "test")
    finfo_list = get_file_list("../")
    for finfo in finfo_list:
        print(finfo.toJson())

    print( "test recursive")
    finfo_list = get_file_list("../", recursive=True)
    for finfo in finfo_list:
        print(finfo.toJson())

    print( "test recursive with ext")
    finfo_list = get_file_list("../", recursive=True, filter_dict={"ext":"py"})
    for finfo in finfo_list:
        print(finfo.toJson())
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
if __name__ == "__main__": test()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
