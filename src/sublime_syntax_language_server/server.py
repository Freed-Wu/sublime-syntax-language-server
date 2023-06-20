r"""Server
==========
"""
import json
import os
import re
from subprocess import CalledProcessError, check_output  # nosec: B404
from typing import Any, Literal, Tuple

from lsprotocol.types import (
    INITIALIZE,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_HOVER,
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionParams,
    Diagnostic,
    DidChangeTextDocumentParams,
    Hover,
    InitializeParams,
    MarkupContent,
    MarkupKind,
    Position,
    Range,
    TextDocumentPositionParams,
)
from platformdirs import user_cache_dir
from pygls.server import LanguageServer

# https://github.com/iamcco/coc-diagnostic/pull/136/files
PAT = 'Assertion selector "[^"]+" from line (\\d+) failed against line \\d+, column range (\\d+)-(\\d+) \\(with text "[^"]+"\\) has scope \\[([^\\]]+)\\]'


def check_extension(uri: str) -> Literal["sublime-syntax", "syntax_test", ""]:
    r"""Check extension.

    :param uri:
    :type uri: str
    :rtype: Literal["sublime-syntax", "syntax_test", ""]
    """
    if uri.split(os.path.extsep)[-1] == "sublime-syntax":
        return "sublime-syntax"
    if os.path.basename(uri).startswith("syntax_test_"):
        return "syntax_test"
    return ""


def diagnostic(
    path: str, syntax_path: str = "."
) -> dict[tuple[int, int, int], str]:
    r"""Diagnostic.

    :param path:
    :type path: str
    :param syntax_path:
    :type syntax_path: str
    :rtype: dict[tuple[int, int, int], str]
    """
    try:
        check_output(  # nosec: B603 B607
            ["syntest", path, syntax_path], universal_newlines=True
        )
        return {}
    except CalledProcessError as e:
        lines = e.output.splitlines()
    results = {}
    for line in lines:
        m = re.match(PAT, line.strip())
        if m is None:
            continue
        results[(m[1], m[2], m[3])] = m[4]
    return results


def get_document(
    method: Literal["builtin", "cache", "web"] = "builtin"
) -> dict[str, str]:
    r"""Get document. ``builtin`` will use builtin sublime-syntax.json. ``cache``
    will generate a cache from
    `<https://www.sublimetext.com/docs/scope_naming.html>`_. ``web`` is same as
    ``cache`` except it doesn't generate cache. We use ``builtin`` as default.
    If you want to get the latest result from
    `<https://www.sublimetext.com/docs/scope_naming.html>`_, you need to
    install `beautifulsoup4 <https://pypi.org/project/beautifulsoup4>` by
    ``pip install 'sublime-syntax-language-server[web]'``.

    :param method:
    :type method: Literal["builtin", "cache", "web"]
    :rtype: dict[str, str]
    """
    if method == "builtin":
        file = os.path.join(
            os.path.join(
                os.path.join(os.path.dirname(__file__), "assets"), "json"
            ),
            "sublime-syntax.json",
        )
        with open(file, "r") as f:
            document = json.load(f)
    elif method == "cache":
        from .api import init_document

        if not os.path.exists(user_cache_dir("sublime-syntax.json")):
            document = init_document()
            with open(user_cache_dir("sublime-syntax.json"), "w") as f:
                json.dump(document, f)
        else:
            with open(user_cache_dir("sublime-syntax.json"), "r") as f:
                document = json.load(f)
    else:
        from .api import init_document

        document = init_document()
    return document


class SublimeSyntaxLanguageServer(LanguageServer):
    r"""Sublime syntax language server."""

    def __init__(self, *args: Any) -> None:
        r"""Init.

        :param args:
        :type args: Any
        :rtype: None
        """
        super().__init__(*args)
        self.document = {}

        @self.feature(INITIALIZE)
        def initialize(params: InitializeParams) -> None:
            r"""Initialize.

            :param params:
            :type params: InitializeParams
            :rtype: None
            """
            opts = params.initialization_options
            method = getattr(opts, "method", "builtin")
            self.document = get_document(method)  # type: ignore

        @self.feature(TEXT_DOCUMENT_HOVER)
        def hover(params: TextDocumentPositionParams) -> Hover | None:
            r"""Hover.

            :param params:
            :type params: TextDocumentPositionParams
            :rtype: Hover | None
            """
            if not check_extension(params.text_document.uri):
                return None
            word = self._cursor_word(
                params.text_document.uri, params.position, True
            )
            if not word:
                return None
            doc = self.document.get(word[0])
            if not doc:
                return None
            return Hover(
                contents=MarkupContent(kind=MarkupKind.PlainText, value=doc),
                range=word[1],
            )

        @self.feature(TEXT_DOCUMENT_COMPLETION)
        def completions(params: CompletionParams) -> CompletionList:
            r"""Completions.

            :param params:
            :type params: CompletionParams
            :rtype: CompletionList
            """
            if not check_extension(params.text_document.uri):
                return CompletionList(is_incomplete=False, items=[])
            word = self._cursor_word(
                params.text_document.uri, params.position, False
            )
            token = "" if word is None else word[0]
            items = [
                CompletionItem(
                    label=x,
                    kind=CompletionItemKind.Variable,
                    documentation=self.document[x],
                    insert_text=x,
                )
                for x in self.document
                if x.startswith(token)
            ]
            return CompletionList(is_incomplete=False, items=items)

        @self.feature(TEXT_DOCUMENT_DID_OPEN)
        @self.feature(TEXT_DOCUMENT_DID_CHANGE)
        def did_change(params: DidChangeTextDocumentParams) -> None:
            r"""Did change.

            :param params:
            :type params: DidChangeTextDocumentParams
            :rtype: None
            """
            doc = self.workspace.get_document(params.text_document.uri)
            if doc.path is None:
                return None
            diagnostics = [
                Diagnostic(
                    range=Range(
                        Position(line, col),
                        Position(line, endcol),
                    ),
                    message=msg,
                    source="pip-compile",
                )
                for (line, col, endcol), msg in diagnostic(doc.path).items()
            ]
            self.publish_diagnostics(doc.uri, diagnostics)

    def _cursor_line(self, uri: str, position: Position) -> str:
        r"""Cursor line.

        :param uri:
        :type uri: str
        :param position:
        :type position: Position
        :rtype: str
        """
        doc = self.workspace.get_document(uri)
        content = doc.source
        line = content.split("\n")[position.line]
        return str(line)

    def _cursor_word(
        self, uri: str, position: Position, include_all: bool = True
    ) -> Tuple[str, Range] | None:
        r"""Cursor word.

        :param uri:
        :type uri: str
        :param position:
        :type position: Position
        :param include_all:
        :type include_all: bool
        :rtype: Tuple[str, Range] | None
        """
        line = self._cursor_line(uri, position)
        cursor = position.character
        for m in re.finditer(r"[\.\w]+", line):
            end = m.end() if include_all else cursor
            if m.start() <= cursor <= m.end():
                word = (
                    line[m.start() : end],
                    Range(
                        start=Position(
                            line=position.line, character=m.start()
                        ),
                        end=Position(line=position.line, character=end),
                    ),
                )
                return word
        return None
