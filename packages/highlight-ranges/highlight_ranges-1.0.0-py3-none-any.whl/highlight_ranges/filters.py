"""Pygments filter that uses spor to highlight ranges of code.
"""
import pathlib

from pygments.filter import Filter
from pygments.token import Generic
from spor.repository import open_repository


class SporRangeFilter(Filter):
    """A pygments filter that adds highlights to code based on spor metadata.

    This looks for spor anchors with metadata of the form `{"highlight": true}`.
    This will then mark the tokens contained in these anchors with
    `Generic.Emph` so that they are highlighted in pygments output.

    Args:
        anchors: An iterable of spor anchors to use.
    """

    def __init__(self, **options):
        super().__init__(**options)
        file_path = pathlib.Path(options['file'])
        repo = open_repository(file_path)
        self._anchors = tuple(anchor for _, anchor in repo.items()
                              if anchor.file_path == file_path.absolute())

    def _should_highlight(self, start, stop):
        "Whether the range `[start,stop]` should be highlighted."
        for anchor in self._anchors:
            if anchor.metadata.get('highlight', False):
                return (start >= anchor.context.offset and
                        stop <= (anchor.context.offset + len(anchor.context.topic)))

        return False

    def filter(self, lexer, stream):
        """Apply anchors to a stream of token to add highlighting.
        """
        start = 0
        for ttype, value in stream:
            stop = start + len(value)
            if self._should_highlight(start, stop):
                ttype = Generic.Emph
            yield ttype, value

            start = stop
