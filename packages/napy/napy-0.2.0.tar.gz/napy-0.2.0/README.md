# Table of Contents

-   [Prologue](#orgc3e7e93)
-   [Introduction](#orgffe4a15)
-   [Usage](#org3e41b5d)
    -   [Tools (Libs)](#org75be8ea)
        -   [Utility](#org5187c6d)
            -   [Flatten](#org4dc4959)
    -   [Comand Line Tools](#org362a745)
        -   [Template](#orgfed4975)
            -   [Crawler](#org7e38b2f)
    -   [More](#orga688170)
-   [Packages](#orgbaebdc2)
    -   [Normal](#orgc103f51)
    -   [Science](#org1d2e8d4)
    -   [Crawler](#org7fd4505)
    -   [Development](#org128bc86)
-   [Epoligue](#org4373da3)
    -   [History](#org97e2dfc)
        -   [0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>](#org634c281)
        -   [0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>](#org751f9a5)

Here is everything frequently use in python.


<a id="orgc3e7e93"></a>

# Prologue

I often need to configure a new Python development environment.  Whether it is to help others or for
myself, it is very troublesome to manage packages with pip.  Besides, there are fascinating and
impressive ipython extensions, and every installation of them has to bother Google again.

Therefore, I created this napy.

*This package is still under development, and although is only for myself now, you can use it as you
like.*


<a id="orgffe4a15"></a>

# Introduction

Napy includes some packages that I frequently use in python, such as `requests`, for crawlers; `sympy`
for mathematics.  Also, napy has some ipython extensions I write.  A template Napy also has that I
often use (of course, it's still straightforward now).  Hope you like it.

*Due to the `.dir-local.el` contains `(org-html-klipsify-src . nil)`, it is warning that it is not safe.*


<a id="org3e41b5d"></a>

# Usage


<a id="org75be8ea"></a>

## Tools (Libs)


<a id="org5187c6d"></a>

### Utility


<a id="org4dc4959"></a>

#### Flatten

Flatten list of iterable objects.

    from napy.tools import flatten, flatten_str

    list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]]))
    # [1, 2, "ab", 3, "c", 4, "d"]

    list(flatten("abc"))
    # ["a", "b", "c"]
    # regard "abc" as ["a", "b", "c"]

    list(flatten_str([1, 2, "ab", [3, "c", [4, ["d"]]]]))
    # or list(flatten([1, 2, "ab", [3, "c", [4, ["d"]]]], True))
    # [1, 2, "a", "b", 3, "c", 4, "d"]


<a id="org362a745"></a>

## Comand Line Tools


<a id="orgfed4975"></a>

### Template


<a id="org7e38b2f"></a>

#### Crawler

    $ napy template --help
    Usage:
      template [options]

    Options:
      -c, --category[=CATEGORY]       Category of template
      -o, --output[=OUTPUT]           Output file (default: "stdout")
      -y, --yes                       Confirmation
      -h, --help                      Display this help message
      -q, --quiet                     Do not output any message
      -V, --version                   Display this application version
          --ansi                      Force ANSI output
          --no-ansi                   Disable ANSI output
      -n, --no-interaction            Do not ask any interactive question
      -v|vv|vvv, --verbose[=VERBOSE]  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug

    Help:
     Template command line tool.

It will generate this:

    from requests_html import HtmlSession as s
    import requests as req


    def crawler() -> None:
        """Crawler."""
        pass


    if __name__ == "__main__":
        pass


<a id="orga688170"></a>

## More

Still under development.


<a id="orgbaebdc2"></a>

# Packages


<a id="orgc103f51"></a>

## Normal

-   **better\_exceptions:** Pretty and helpful exceptions, automatically.
-   **pendulum:** Python datetimes made easy.
-   **tqdm:** Fast, Extensible Progress Meter.


<a id="org1d2e8d4"></a>

## Science

-   **jupyter :: Jupyter Notebook + IPython:** Jupyter metapackage. Install all the Jupyter components in
    one go.
-   **numpy:** NumPy: array processing for numbers, strings, records, and objects
-   **pandas:** Powerful data structures for data analysis, time series, and statistics
-   **sympy:** Computer algebra system (CAS) in Python


<a id="org7fd4505"></a>

## Crawler

-   **requests:** Python HTTP for Humans.
-   **requests\_html:** HTML Parsing for Humans.
-   **BeautifulSoup4:** Screen-scraping library


<a id="org128bc86"></a>

## Development

-   **cleo:** Cleo allows you to create beautiful and testable command-line interfaces.


<a id="org4373da3"></a>

# Epoligue


<a id="org97e2dfc"></a>

## History


<a id="org634c281"></a>

### 0.1.1 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-17 Mon&gt;</span></span>

Use README.md instead of README.org


<a id="org751f9a5"></a>

### 0.1.0 <span class="timestamp-wrapper"><span class="timestamp">&lt;2018-12-16 Sun&gt;</span></span>

-   The beginning of everything
