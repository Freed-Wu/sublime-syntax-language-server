r"""Api
=======
"""
import sys
from urllib import request

from bs4 import BeautifulSoup, FeatureNotFound
from bs4.element import Tag

URI = "https://www.sublimetext.com/docs/scope_naming.html"


def init_document() -> dict[str, str]:
    r"""Init document.

    :rtype: dict[str, str]
    """
    with request.urlopen(URI) as f:  # nosec: B310
        html = f.read()

    try:
        soup = BeautifulSoup(html, "lxml")
    except FeatureNotFound:
        soup = BeautifulSoup(html, "html.parser")

    items = {}
    reference = soup.find(id="alphabetical-reference")
    if not isinstance(reference, Tag):
        sys.exit("alphabetical-reference is not Tag!")
    p = reference.find("p")
    if not isinstance(p, Tag):
        sys.exit("p is not Tag!")
    info = p.get_text().replace("\n", " ").strip()
    ul = reference.find("ul")
    if not isinstance(ul, Tag):
        sys.exit("ul is not Tag!")
    for li in ul.find_all("li"):
        word = li.get_text().strip(".")
        items[word] = info
    for section in reference.find_all("section"):
        for ul in section.find_all("ul"):
            p = ul.find_previous("p")
            info = p.get_text().replace("\n", " ").strip()
            for li in ul.find_all("li"):
                word = li.get_text()
                items[word] = info
    return items
