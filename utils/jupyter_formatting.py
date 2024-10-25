# utils/jupyter_formatting.py
import json
import textwrap
import typing

from IPython.core import getipython
from IPython.lib import pretty
import numpy as np


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def setup_notebook_formatting():
    def pretty_print_formatter(
        obj: typing.Union[
            dict, list, typing.Any
        ],  # The object to be formatted - either dict, list, or any other type
        p: pretty.PrettyPrinter,  # IPython's pretty printer object that handles the output
        cycle: bool,  # Boolean flag indicating if we've detected a recursive cycle
    ) -> None:  # Function returns None as p.text() handles the output
        if cycle:
            return p.text('...')
        if isinstance(obj, (dict, list)):
            formatted = json.dumps(obj, indent=4, cls=CustomJSONEncoder)
            wrapped_lines = [
                textwrap.fill(
                    line, width=99, subsequent_indent=' ' * (line.find(line.lstrip()[0]))
                )
                for line in formatted.split('\n')
            ]
            p.text('\n'.join(wrapped_lines))
        else:
            p.text(repr(obj))

    # Get IPython instance
    ip = getipython.get_ipython()

    # Register the formatter for plain text
    ip.display_formatter.formatters['text/plain'].for_type(dict, pretty_print_formatter)
    ip.display_formatter.formatters['text/plain'].for_type(list, pretty_print_formatter)
