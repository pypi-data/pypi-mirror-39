import os

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

_isNotDumb = os.getenv("TERM", "dumb").lower() != "dumb"

# Scroll actions
SCROLL_LINE_UP = "line up"
SCROLL_LINE_DOWN = "line down"
SCROLL_PAGE_UP = "page up"
SCROLL_PAGE_DOWN = "page down"
SCROLL_TO_TOP = "to top"
SCROLL_TO_END = "to end"

# ASCII color codes
YELLOW = '\033[33m' if _isNotDumb else ''
RED = "\033[31m" if _isNotDumb else ''
BOLD = '\033[1m' if _isNotDumb else ''
UNDERLINE = '\033[4m' if _isNotDumb else ''
END = "\033[0m" if _isNotDumb else ''
