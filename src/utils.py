import re

from enums import ParseMode


def fmt(text, **kwargs):
    if text["parse_mode"] == ParseMode.MARKDOWN_V2:
        kwargs = {k: escape_markdown_v2(v) for k, v in kwargs.items()}

    return text["text"].format(**kwargs)


def escape_markdown_v2(text):
    return re.sub(r"([_*[\]()~`>#+\-=|{}.!])", r"\\\1", text)


def filter_none(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}
