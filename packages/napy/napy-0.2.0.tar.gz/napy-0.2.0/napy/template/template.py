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
date     : Dec 13, 2018
email    : Nasy <nasyxx+python@gmail.com>
filename : default.py
project  : napy.template
license  : GPL-3.0+

There are more things in heaven and earth, Horatio, than are dreamt.
 --  From "Hamlet"

Templates.

Templates will be generated but will not be formatted.  You may format your
  code later.
"""
# Standard Library
from typing import List, NewType, Optional, NamedTuple

Package = NamedTuple(
    "Package",
    [
        # Format
        # from {name} import {module} as {alias}
        # import {module} as {alias}
        ("name", Optional[str]),
        ("module", str),
        ("alias", Optional[str]),
    ],
)
Function = NamedTuple(
    "Function", [("name", str), ("description", str), ("res", Optional[str])]
)
Epoligue = NewType("Epoligue", str)
Template = NamedTuple(
    "Template",
    [
        ("packages", List[Package]),
        ("functions", List[Function]),
        ("epoligue", Epoligue),
    ],
)


def package_to_str(package: Package) -> str:
    """Package to string."""
    return (
        (f"from {package.name} " if package.name else "")
        + (f"import {package.module}")
        + (f" as {package.alias}" if package.alias else "")
    )


def function_to_str(function: Function) -> str:
    """Function to string."""
    return "\n".join(
        (
            f"def {function.name}()"
            + (f" -> {function.res}" if function.res else "")
            + ":",
            f'    """{function.description}"""',
            "    pass",
        )
    )


def to_str(template: Template) -> str:
    """Template to string."""
    return "\n\n\n".join(
        (
            "\n".join(map(package_to_str, template.packages)),
            "\n\n\n".join(map(function_to_str, template.functions)),
            template.epoligue,
        )
    )


def crawler() -> Template:
    """Generate crawler template."""
    return Template(
        [
            Package("requests_html", "HtmlSession", "s"),
            Package(None, "requests", "req"),
        ],
        [Function("crawler", "Crawler.", "None")],
        Epoligue('if __name__ == "__main__":\n    pass\n'),
    )
