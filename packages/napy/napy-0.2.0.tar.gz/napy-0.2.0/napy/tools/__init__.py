#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Life's pathetic, have fun ("▔□▔)/hi~♡ Nasy.

Excited without bugs::

    |             *         *
    |                  .                .
    |           .
    |     *                      ,
    |                   .
    |
    |                               *
    |          |\___/|
    |          )    -(             .              ·
    |         =\ -   /=
    |           )===(       *
    |          /   - \
    |          |-    |
    |         /   -   \     0.|.0
    |  NASY___\__( (__/_____(\=/)__+1s____________
    |  ______|____) )______|______|______|______|_
    |  ___|______( (____|______|______|______|____
    |  ______|____\_|______|______|______|______|_
    |  ___|______|______|______|______|______|____
    |  ______|______|______|______|______|______|_
    |  ___|______|______|______|______|______|____

author   : Nasy https://nasy.moe
date     : Dec 17, 2018
email    : Nasy <nasyxx+python@gmail.com>
filename : __init__.py
project  : napy.tools
license  : GPL-3.0+

There are more things in heaven and earth, Horatio, than are dreamt.
 --  From "Hamlet"
"""
# Local Packages
from .utility import flatten, flatten_str

if __name__ == "__main__":
    assert list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]])) == [
        1,
        2,
        "ab",
        3,
        "c",
        4,
        "d",
    ]
    assert list(flatten_str([1, 2, "ab", [3, "c", [4, ["d"]]]])) == [
        1,
        2,
        "a",
        "b",
        3,
        "c",
        4,
        "d",
    ]
