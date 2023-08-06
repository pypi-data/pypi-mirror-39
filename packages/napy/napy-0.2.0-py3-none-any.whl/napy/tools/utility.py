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
filename : utility.py
project  : napy.tools
license  : GPL-3.0+

There are more things in heaven and earth, Horatio, than are dreamt.
 --  From "Hamlet"
"""
# Standard Library
from typing import Union, TypeVar, Iterable, Generator
from collections import Iterable as Iterable_

# Typing
a = TypeVar("a")
Ia = Iterable[a]
MIa = Iterable[Iterable[a]]
iterable_ = Union[Ia, MIa]


def flatten(i: iterable_, string: bool = False) -> Generator[Ia, None, None]:
    """Flatten list of iterable objects."""
    for ii in i:
        if (
            isinstance(ii, Iterable_)
            and not isinstance(ii, str)
            or isinstance(ii, str)
            and string
            and len(ii) > 1
        ):
            for iii in flatten(ii, string):
                yield iii
        else:
            yield ii


def flatten_str(i: iterable_) -> Generator[Ia, None, None]:
    """Flatten list of iterable objects, even if they are strings."""
    for ii in flatten(i, True):
        yield ii
