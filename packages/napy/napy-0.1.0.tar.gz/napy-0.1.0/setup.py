# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['napy', 'napy.console', 'napy.ipyext', 'napy.template']

package_data = \
{'': ['*']}

install_requires = \
['better_exceptions>=0.2.1,<0.3.0',
 'cleo>=0.7.2,<0.8.0',
 'requests>=2.21,<3.0',
 'requests_html>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['napy = napy.console:run']}

setup_kwargs = {
    'name': 'napy',
    'version': '0.1.0',
    'description': 'Everything you frequently use when you use python.',
    'long_description': '#+OPTIONS: \':nil *:t -:t ::t <:t H:3 \\n:nil ^:{} arch:headline author:t\n#+OPTIONS: broken-links:nil c:nil creator:nil d:(not "LOGBOOK") date:t e:t\n#+OPTIONS: email:nil f:t inline:t num:nil p:nil pri:nil prop:nil stat:t tags:t\n#+OPTIONS: tasks:t tex:t timestamp:t title:t toc:t todo:t |:t\n#+TITLE: Napy\n#+DATE: <2018-12-11 Tue>\n#+AUTHOR: Nasy\n#+EMAIL: nasyxx@gmail.com\n#+LANGUAGE: en\n#+SELECT_TAGS: export\n#+EXCLUDE_TAGS: noexport\n#+CREATOR: Emacs 27.0.50 (Org mode 9.1.9)\n\n#+SETUPFILE: https://fniessen.github.io/org-html-themes/setup/theme-readtheorg.setup\n\nEverything you frequently use when you use Python.\n\n* Prologue\n\nI often need to configure a new Python development environment.  Whether it is to help others or for\nmyself, it is very troublesome to manage packages with pip.  Besides, there are fascinating and\nimpressive ipython extensions, and every installation of them has to bother Google again.\n\nTherefore, I created this napy.\n\n/This package is still under development, and although is only for myself now, you can use it as you\nlike./\n\n* Introduction\n\nNapy includes some of the packages I frequently use, such as ~requests~, for crawlers; ~sympy~ for\nmathematics.  Also, napy has some ipython extensions I write.  A template Napy also has that I often\nuse (of course, it\'s still straightforward now).  Hope you like it.\n\n/Due to the ~.dir-local.el~ contains ~(org-html-klipsify-src . nil)~, it is warning that it is not safe./\n\n* Usage\n\n** Template\n\n*** Crawler\n\n#+begin_src shell\n  $ napy template --help\n  Usage:\n    template [options]\n\n  Options:\n    -c, --category[=CATEGORY]       Category of template\n    -o, --output[=OUTPUT]           Output file (default: "stdout")\n    -y, --yes                       Confirmation\n    -h, --help                      Display this help message\n    -q, --quiet                     Do not output any message\n    -V, --version                   Display this application version\n        --ansi                      Force ANSI output\n        --no-ansi                   Disable ANSI output\n    -n, --no-interaction            Do not ask any interactive question\n    -v|vv|vvv, --verbose[=VERBOSE]  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug\n\n  Help:\n   Template command line tool.\n#+end_src\n\nIt will generate this:\n\n#+begin_src python\n  from requests_html import HtmlSession as s\n  import requests as req\n\n\n  def crawler() -> None:\n      """Crawler."""\n      pass\n\n\n  if __name__ == "__main__":\n      pass\n#+end_src\n\n** More\n\nStill under development.\n\n* Packages\n\n** Normal\n\n+ better_exceptions :: Pretty and helpful exceptions, automatically.\n+ pendulum :: Python datetimes made easy.\n+ tqdm :: Fast, Extensible Progress Meter.\n\n** Science\n\n+ jupyter :: Jupyter Notebook + IPython :: Jupyter metapackage. Install all the Jupyter components in\n     one go.\n+ numpy :: NumPy: array processing for numbers, strings, records, and objects\n+ pandas :: Powerful data structures for data analysis, time series, and statistics\n+ sympy :: Computer algebra system (CAS) in Python\n\n** Crawler\n\n+ requests :: Python HTTP for Humans.\n+ requests_html :: HTML Parsing for Humans.\n+ BeautifulSoup4 :: Screen-scraping library\n\n** Development\n\n+ cleo :: Cleo allows you to create beautiful and testable command-line interfaces.\n\n* Epoligue\n\n** History\n\n#+include: "CHANGELOG" :minlevel 3\n',
    'author': 'Nasy',
    'author_email': 'nasyxx+napy@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
