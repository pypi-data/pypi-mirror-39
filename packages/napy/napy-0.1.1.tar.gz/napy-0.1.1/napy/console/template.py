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
date     : Dec 14, 2018
email    : Nasy <nasyxx+python@gmail.com>
filename : console.py
project  : napy.console
license  : GPL-3.0+

There are more things in heaven and earth, Horatio, than are dreamt.
 --  From "Hamlet"
"""
# Standard Library
import os

# Command Line Tools
from cleo import Command

# Local Packages
from ..template import to_str, crawler


class TemplateCommand(Command):
    """Template command line tool.

    template
        {--c|category=? : Category of template}
        {--o|output=? : Output file (default: "stdout")}
        {--y|yes : Confirmation}
    """

    def handle(self) -> None:
        """Handle template command."""
        category = self.option("category") or self.choice(
            "<options=bold;options=underscore>"
            "Select a category (default: crawler)</>",
            ["crawler"],
            0,
        )

        question = self.create_question(
            "<options=bold;options=underscore>"
            "Output file (default: <stdout>):</>"
        )
        question.set_autocomplete_values(
            list(filter(lambda x: x.endswith(".py"), os.listdir(".")))
        )
        output = self.option("output") or self.ask(question) or "<stdout>"

        template = to_str({"crawler": crawler}[category]())

        if self.option("yes") or self.confirm(
            "<options=bold;options=underscore>"
            "Continue with this action?"
            "</>\n"
            "<fg=green;options=bold>Write template to </>"
            f"<fg=magenta>{output}</>\n",
            default=True,
        ):
            if output != "<stdout>":
                with open(output, "a") as f:
                    f.write(template)
            else:
                self.line(
                    "<fg=red>---------</>\n"
                    f"<fg=cyan;options=bold>{template}</>\n"
                    "<fg=red>---------</>\n"
                )
        else:
            self.line("<info>Fine.</info>")
