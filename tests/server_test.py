r"""Test server"""

import os
from shutil import which

import pytest

from sublime_syntax_language_server.server import diagnostic, get_document

PATH = "syntax_test_requirements.txt"


class Test:
    r"""Test."""

    @staticmethod
    def test_get_document() -> None:
        r"""Test get document.

        :rtype: None
        """
        assert len(get_document().get("comment.line", "").splitlines())

    @staticmethod
    @pytest.mark.skipif(
        which("syntest") is None, reason="syntest must be installed"
    )
    def test_diagnostic() -> None:
        r"""Test diagnostic.

        :rtype: None
        """
        os.chdir(os.path.dirname(__file__))
        result = diagnostic(PATH)
        expected = {
            (
                "82",
                "48",
                "58",
            ): "<source.requirements-txt>, <markup.underline.link.url.requirements-txt>"
        }
        assert result == expected
