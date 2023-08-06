# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['napy', 'napy.console', 'napy.ipyext', 'napy.template', 'napy.tools']

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
    'version': '0.2.0',
    'description': 'Here is everything frequently use in python.',
    'long_description': '# Table of Contents\n\n-   [Prologue](#orgc3e7e93)\n-   [Introduction](#orgffe4a15)\n-   [Usage](#org3e41b5d)\n    -   [Tools (Libs)](#org75be8ea)\n        -   [Utility](#org5187c6d)\n            -   [Flatten](#org4dc4959)\n    -   [Comand Line Tools](#org362a745)\n        -   [Template](#orgfed4975)\n            -   [Crawler](#org7e38b2f)\n    -   [More](#orga688170)\n-   [Packages](#orgbaebdc2)\n    -   [Normal](#orgc103f51)\n    -   [Science](#org1d2e8d4)\n    -   [Crawler](#org7fd4505)\n    -   [Development](#org128bc86)\n-   [Epoligue](#org4373da3)\n    -   [History](#org97e2dfc)\n        -   [0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>](#org634c281)\n        -   [0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>](#org751f9a5)\n\nHere is everything frequently use in python.\n\n\n<a id="orgc3e7e93"></a>\n\n# Prologue\n\nI often need to configure a new Python development environment.  Whether it is to help others or for\nmyself, it is very troublesome to manage packages with pip.  Besides, there are fascinating and\nimpressive ipython extensions, and every installation of them has to bother Google again.\n\nTherefore, I created this napy.\n\n*This package is still under development, and although is only for myself now, you can use it as you\nlike.*\n\n\n<a id="orgffe4a15"></a>\n\n# Introduction\n\nNapy includes some packages that I frequently use in python, such as `requests`, for crawlers; `sympy`\nfor mathematics.  Also, napy has some ipython extensions I write.  A template Napy also has that I\noften use (of course, it\'s still straightforward now).  Hope you like it.\n\n*Due to the `.dir-local.el` contains `(org-html-klipsify-src . nil)`, it is warning that it is not safe.*\n\n\n<a id="org3e41b5d"></a>\n\n# Usage\n\n\n<a id="org75be8ea"></a>\n\n## Tools (Libs)\n\n\n<a id="org5187c6d"></a>\n\n### Utility\n\n\n<a id="org4dc4959"></a>\n\n#### Flatten\n\nFlatten list of iterable objects.\n\n    from napy.tools import flatten, flatten_str\n\n    list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]]))\n    # [1, 2, "ab", 3, "c", 4, "d"]\n\n    list(flatten("abc"))\n    # ["a", "b", "c"]\n    # regard "abc" as ["a", "b", "c"]\n\n    list(flatten_str([1, 2, "ab", [3, "c", [4, ["d"]]]]))\n    # or list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]], True))\n    # [1, 2, "a", "b", 3, "c", 4, "d"]\n\n\n<a id="org362a745"></a>\n\n## Comand Line Tools\n\n\n<a id="orgfed4975"></a>\n\n### Template\n\n\n<a id="org7e38b2f"></a>\n\n#### Crawler\n\n    $ napy template --help\n    Usage:\n      template [options]\n\n    Options:\n      -c, --category[=CATEGORY]       Category of template\n      -o, --output[=OUTPUT]           Output file (default: "stdout")\n      -y, --yes                       Confirmation\n      -h, --help                      Display this help message\n      -q, --quiet                     Do not output any message\n      -V, --version                   Display this application version\n          --ansi                      Force ANSI output\n          --no-ansi                   Disable ANSI output\n      -n, --no-interaction            Do not ask any interactive question\n      -v|vv|vvv, --verbose[=VERBOSE]  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug\n\n    Help:\n     Template command line tool.\n\nIt will generate this:\n\n    from requests_html import HtmlSession as s\n    import requests as req\n\n\n    def crawler() -> None:\n        """Crawler."""\n        pass\n\n\n    if __name__ == "__main__":\n        pass\n\n\n<a id="orga688170"></a>\n\n## More\n\nStill under development.\n\n\n<a id="orgbaebdc2"></a>\n\n# Packages\n\n\n<a id="orgc103f51"></a>\n\n## Normal\n\n-   **better\\_exceptions:** Pretty and helpful exceptions, automatically.\n-   **pendulum:** Python datetimes made easy.\n-   **tqdm:** Fast, Extensible Progress Meter.\n\n\n<a id="org1d2e8d4"></a>\n\n## Science\n\n-   **jupyter :: Jupyter Notebook + IPython:** Jupyter metapackage. Install all the Jupyter components in\n    one go.\n-   **numpy:** NumPy: array processing for numbers, strings, records, and objects\n-   **pandas:** Powerful data structures for data analysis, time series, and statistics\n-   **sympy:** Computer algebra system (CAS) in Python\n\n\n<a id="org7fd4505"></a>\n\n## Crawler\n\n-   **requests:** Python HTTP for Humans.\n-   **requests\\_html:** HTML Parsing for Humans.\n-   **BeautifulSoup4:** Screen-scraping library\n\n\n<a id="org128bc86"></a>\n\n## Development\n\n-   **cleo:** Cleo allows you to create beautiful and testable command-line interfaces.\n\n\n<a id="org4373da3"></a>\n\n# Epoligue\n\n\n<a id="org97e2dfc"></a>\n\n## History\n\n\n<a id="org634c281"></a>\n\n### 0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>\n\nUse README.md instead of README.org\n\n\n<a id="org751f9a5"></a>\n\n### 0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>\n\n-   The beginning of everything\n',
    'author': 'Nasy',
    'author_email': 'nasyxx+napy@gmail.com',
    'url': 'https://nasyxx.gitlab.io/napy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
