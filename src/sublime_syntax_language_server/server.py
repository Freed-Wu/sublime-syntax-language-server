r"""Server
==========
"""

import json
import os
import re
from subprocess import CalledProcessError, check_output  # nosec: B404
from typing import Any, Literal, Tuple

from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_HOVER,
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionOptions,
    CompletionParams,
    Diagnostic,
    DiagnosticSeverity,
    DidChangeTextDocumentParams,
    Hover,
    MarkupContent,
    MarkupKind,
    Position,
    Range,
    TextDocumentPositionParams,
)
from pygls.server import LanguageServer


class SublimeSyntaxLanguageServer(LanguageServer):
    r"""Sublime syntax language server."""

    # https://github.com/iamcco/coc-diagnostic/pull/136/files
    regex = re.compile(
        'Assertion selector "[^"]+" from line (\\d+) failed against line \\d+, column range (\\d+)-(\\d+) \\(with text "[^"]+"\\) has scope \\[([^\\]]+)\\]'
    )

    def __init__(self, *args: Any) -> None:
        r"""Init.

        :param args:
        :type args: Any
        :rtype: None
        """
        super().__init__(*args)
        file = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "json",
            "sublime-syntax.json",
        )
        with open(file) as f:
            self.document = json.load(f)

        @self.feature(TEXT_DOCUMENT_HOVER)
        def hover(params: TextDocumentPositionParams) -> Hover | None:
            r"""Hover.

            :param params:
            :type params: TextDocumentPositionParams
            :rtype: Hover | None
            """
            if not self.check_extension(params.text_document.uri):
                return None
            word = self._cursor_word(
                params.text_document.uri, params.position, True
            )
            if not word:
                return None
            keyword = word[0]
            keyword, doc = self.search_doc(self.document, keyword)
            if doc == "" or keyword == "":
                return None
            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.PlainText, value=keyword + "\n" + doc
                ),
                range=word[1],
            )

        @self.feature(
            TEXT_DOCUMENT_COMPLETION,
            CompletionOptions(trigger_characters=["."]),
        )
        def completion(params: CompletionParams) -> CompletionList:
            r"""Complete.

            :param params:
            :type params: CompletionParams
            :rtype: CompletionList
            """
            if not self.check_extension(params.text_document.uri):
                return CompletionList(is_incomplete=False, items=[])
            word = self._cursor_word(
                params.text_document.uri, params.position, False
            )
            keyword = "" if word is None else word[0]
            prefix, mid, _ = keyword.rpartition(".")
            length = len(prefix + mid)
            items = [
                CompletionItem(
                    label=x,
                    kind=CompletionItemKind.Variable,
                    documentation=self.document[x],
                    insert_text=x[length:],
                )
                for x in self.document
                if x.startswith(keyword)
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
                    severity=DiagnosticSeverity.Error,
                )
                for (line, col, endcol), msg in self.diagnostic(
                    doc.path
                ).items()
            ]
            self.publish_diagnostics(doc.uri, diagnostics)

    @staticmethod
    def check_extension(
        uri: str,
    ) -> Literal["sublime-syntax", "syntax_test", ""]:
        r"""Check extension.

        :param uri:
        :type uri: str
        :rtype: Literal["sublime-syntax", "syntax_test", ""]
        """
        basename = os.path.basename(uri)
        if basename.endswith(".sublime-syntax"):
            return "sublime-syntax"
        if basename.startswith("syntax_test_"):
            return "syntax_test"
        return ""

    @staticmethod
    def search_doc(document: dict[str, str], keyword: str) -> tuple[str, str]:
        r"""Search doc.

        :param document:
        :type document: dict[str, str]
        :param keyword:
        :type keyword: str
        :rtype: tuple[str, str]
        """
        doc = document.get(keyword, "")
        while doc == "" and keyword != "":
            keyword, _, _ = keyword.rpartition(".")
            doc = document.get(keyword, "")
        return (keyword, doc)

    def diagnostic(
        self, path: str, syntax_path: str = "."
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
            m = self.regex.match(line.strip())
            if m is None:
                continue
            results[(m[1], m[2], m[3])] = m[4]
        return results

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
