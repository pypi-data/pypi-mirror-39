#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Life's pathetic, have fun ("▔□▔)/hi~♡ Nasy.

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
date     : Dec 12, 2018
email    : Nasy <nasyxx+python@gmail.com>
filename : ns.py
project  : napy.ipyext
license  : GPL-3.0+

There are more things in heaven and earth, Horatio, than are dreamt.
 --  From "Hamlet"

Here are some of the frequently used packages. When I use ipython, I usually
import these packages into the namespaces, which is surprisingly convenient.

Include:
  os
  sys
  random
  re
  itertools.chain           as chain
  pendulum
  time
  pandas                    as pd
  numpy                     as np
  numpy.linalg              as nlg
  requests                  as req
  requests_html.HTMLSession as s
"""

# Other Packages
from IPython.utils.importstring import import_item
from IPython.core.interactiveshell import InteractiveShell

namespaces = {
    "os": "os",
    "sys": "sys",
    "random": "random",
    "re": "re",
    "chain": "itertools.chain",
    "pendulum": "pendulum",
    "time": "time",
    "pd": "pandas",
    "np": "numpy",
    "nlg": "numpy.linalg",
    "req": "requests",
    "s": "requests_html.HTMLSession",
}


def load_ipython_extension(ip: InteractiveShell) -> None:
    """Load ipython extension."""
    ns = ip.user_ns
    for k, v in namespaces.items():
        ns[k] = import_item(v)
