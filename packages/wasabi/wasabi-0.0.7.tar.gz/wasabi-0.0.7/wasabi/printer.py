# coding: utf8
from __future__ import unicode_literals, print_function

from collections import Counter
from contextlib import contextmanager
from multiprocessing import Process
import itertools
import sys
import time

from .tables import table
from .util import wrap, supports_ansi, can_render, locale_escape
from .util import MESSAGES, COLORS, ICONS
from .util import color as _color


class Printer(object):
    def __init__(
        self,
        pretty=True,
        no_print=False,
        colors=None,
        icons=None,
        line_max=80,
        animation="⠙⠹⠸⠼⠴⠦⠧⠇⠏",
        animation_ascii="|/-\\",
        ignore_warnings=False,
    ):
        """Initialize the command-line printer.

        pretty (bool): Pretty-print output (colors, icons).
        no_print (bool): Don't actually print, just return.
        colors (dict): Add or overwrite color values, name mapped to value.
        icons (dict): Add or overwrite icons. Name mapped to unicode icon.
        line_max (int): Maximum line length (for divider).
        animation (unicode): Steps of loading animation for loading() method.
        animation_ascii (unicode): Alternative animation for ASCII terminals.
        ignore_warnings (bool): Do not output messages of type MESSAGE.WARN.
        RETURNS (Printer): The initialized printer.
        """
        self._counts = Counter()
        self.pretty = pretty
        self.no_print = no_print
        self.supports_ansi = supports_ansi()
        self.ignore_warnings = ignore_warnings
        self.line_max = line_max
        self.colors = dict(COLORS)
        self.icons = dict(ICONS)
        if colors:
            self.colors.update(colors)
        if icons:
            self.icons.update(icons)
        self.anim = animation if can_render(animation) else animation_ascii

    @property
    def counts(self):
        """Get the counts of how often the special printers were fired,
        e.g. MESSAGES.GOOD. Can be used to print an overview like "X warnings".
        """
        return self._counts

    def good(self, title="", text="", show=True, exits=None):
        """Print a success message."""
        return self._get_msg(title, text, style=MESSAGES.GOOD, show=show, exits=exits)

    def fail(self, title="", text="", show=True, exits=None):
        """Print an error message."""
        return self._get_msg(title, text, style=MESSAGES.FAIL, show=show, exits=exits)

    def warn(self, title="", text="", show=True, exits=None):
        """Print a warning message."""
        return self._get_msg(title, text, style=MESSAGES.WARN, show=show, exits=exits)

    def info(self, title="", text="", show=True, exits=None):
        """Print an error message."""
        return self._get_msg(title, text, style=MESSAGES.INFO, show=show, exits=exits)

    def text(
        self,
        title="",
        text="",
        color=None,
        icon=None,
        show=True,
        no_print=False,
        exits=None,
    ):
        """Print a message.

        title (unicode): The main text to print.
        text (unicode): Optional additional text to print.
        color (unicode / int): Foreground color.
        icon (unicode): Name of icon to add.
        show (bool): Whether to print or not. Can be used to only output
            messages under certain condition, e.g. if --verbose flag is set.
        no_print (bool): Don't actually print, just return.
        exits (int): Perform a system exit.
        """
        if not show:
            return
        if self.pretty:
            color = self.colors.get(color)
            icon = self.icons.get(icon)
            if icon:
                title = locale_escape("{} {}".format(icon, title)).strip()
            if self.supports_ansi:
                title = _color(title, fg=color)
            title = wrap(title, indent=0)
        if text:
            title = "{}\n{}".format(title, wrap(text, indent=0))
        if exits is not None:
            title = "\n{}\n".format(title)
        if self.no_print or no_print:
            return title
        print(title)
        if exits is not None:
            sys.stdout.flush()
            sys.stderr.flush()
            sys.exit(exits)

    def divider(self, text="", char="=", show=True):
        """Print a divider with a headline:
        ============================ Headline here ===========================

        text (unicode): Headline text. If empty, only the line is printed.
        char (unicode): Line character to repeat, e.g. =.
        show (bool): Whether to print or not.
        """
        if len(char) != 1:
            raise ValueError(
                "Divider chars need to be one character long. "
                "Received: {}".format(char)
            )
        if self.pretty:
            deco = char * (int(round((self.line_max - len(text))) / 2) - 2)
            text = " {} ".format(text) if text else ""
            text = _color(
                "\n{deco}{text}{deco}".format(deco=deco, text=text), bold=True
            )
        if len(text) < self.line_max:
            text = text + char * (self.line_max - len(text))
        if self.no_print:
            return text
        print(text)

    def table(self, data, **kwargs):
        title = kwargs.pop("title", None)
        text = table(data, **kwargs)
        if title:
            self.divider(title)
        if self.no_print:
            return text
        print(text)

    @contextmanager
    def loading(self, text=""):
        sys.stdout.flush()
        t = Process(target=self._spinner, args=(text,))
        t.start()
        try:
            yield
        except Exception as e:
            # Handle exception inside the with block
            t.terminate()
            sys.stdout.write("\n")
            raise (e)
        t.terminate()
        sys.stdout.write("\r\x1b[2K")  # erase line
        sys.stdout.flush()

    def _spinner(self, text="Loading..."):
        for char in itertools.cycle(self.anim):
            sys.stdout.write("\r{} {}".format(char, text))
            sys.stdout.flush()
            time.sleep(0.1)

    def _get_msg(self, title, text, style=None, show=None, exits=None):
        if self.ignore_warnings and style == MESSAGES.WARN:
            show = False
        self._counts[style] += 1
        return self.text(title, text, color=style, icon=style, show=show, exits=exits)
