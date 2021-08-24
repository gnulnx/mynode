import json
from pygments import highlight, lexers, formatters


def format_json(message, indent=4, sort_keys=True, default=str, color=False):
    """
    Take an input string and convert it to a python dictionary and then to a json string
    : return json, dict
    """
    if isinstance(message, dict) or isinstance(message, list):
        msg = message
    else:
        _msg = "".join(message)
        try:
            msg = json.loads(_msg)
        except ValueError:
            msg = message

    formatted_json = json.dumps(msg, indent=4, sort_keys=True, default=str)

    if color:
        return (
            highlight(
                formatted_json,
                lexers.JsonLexer(),
                formatters.TerminalFormatter(),
            ),
            msg,
        )
    else:
        return json.dumps(msg, indent=4, sort_keys=True, default=str), msg


def jprint(message, indent=4, sort_keys=True, default=str, color=True):
    """
    Use this method to pretty print a python dictionary with color.
    """
    _json, _ = format_json(message, indent, sort_keys, default, color)
    print(_json)
    return _json
