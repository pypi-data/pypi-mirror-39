#!/usr/bin/env python3
# -*- coding:utf-8 -*-⏎

from __future__ import print_function
from image import *
from fs import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def test():
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
    src_fi=FileInfo("a.jpg")
    dst_fn="a.thumb.jpg"
    size = (120,100)
    print("a.jpg")
    if save_thumb(src_fi, dst_fn, size):
        print("ok")
    else:
        print("no")

    src_fi=FileInfo("b.jpg")
    dst_fn="b.thumb.jpg"
    size = (120,100)
    print("b.jpg")
    if save_thumb(src_fi, dst_fn, size):
        print("ok")
    else:
        print("no")

    src_fi=FileInfo("c.jpg")
    dst_fn="c.thumb.jpg"
    print("c.jpg")
    size = (120,100)
    if save_thumb(src_fi, dst_fn, size):
        print("ok")
    else:
        print("no")

    src_fi=FileInfo("a.png")
    dst_fn="a.thumb.png.jpg"
    print("a.png")
    size = (120,100)
    if save_thumb(src_fi, dst_fn, size):
        print("ok")
    else:
        print("no")

    src_fi=FileInfo("c.png")
    dst_fn="c.thumb.png.jpg"
    size = (120,100)
    if save_thumb(src_fi, dst_fn, size):
        print("ok")
    else:
        print("no")

if __name__ == "__main__": test()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
