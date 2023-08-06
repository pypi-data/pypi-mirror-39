"""Examples of styles for highlighting.
"""

from pygments.style import Style
from pygments.token import Generic


class BlackOnRed(Style):
    """An example style that highlights with black text on a red background.
    """
    default_style = ""
    styles = {
        Generic.Emph:           'bg:#f00 #fff'
    }
