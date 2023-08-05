# -*- coding: utf-8 -*-

"""
header markups
"""

import attr
from ..base import RstObj

dash_char_list = " _~"
ignore_char_list = """`*()[]{}<>"'"""


def to_label(title):
    for char in dash_char_list:
        title = title.replace(char, "-")
    for char in ignore_char_list:
        title = title.replace(char, "")
    return "-".join([
        chunk.strip() for chunk in title.split("-") if chunk.strip()
    ])


HEADER_CHAR_MAPPER = {
    1: "=",
    2: "-",
    3: "~",
    4: "+",
    5: "*",
    6: "#",
    7: "^",
}


@attr.s
class Header(RstObj):
    title = attr.ib()
    header_level = attr.ib(default=None)
    ref_label = attr.ib(default=None)
    auto_label = attr.ib(default=False)

    _header_level = 0
    _bar_length = None

    meta_not_none_fields = ("header_level",)

    def __attrs_post_init__(self):
        super(Header, self).__attrs_post_init__()
        if self.auto_label and (self.ref_label is None):
            self.ref_label = to_label(self.title)

    @property
    def header_char(self):
        if self.header_level:
            return HEADER_CHAR_MAPPER[self.header_level]
        else:
            return HEADER_CHAR_MAPPER[self._header_level]

    @property
    def template_name(self):
        return "{}.{}.rst".format(self.__module__, "Header")

    def render(self, bar_length=None, **kwargs):
        if bar_length is None:
            self._bar_length = len(self.title)
        else:
            self._bar_length = bar_length
        return super(Header, self).render(**kwargs)


@attr.s
class HeaderLevel(Header):
    meta_not_none_fields = tuple()


@attr.s
class Header1(HeaderLevel):
    """
    Example::

        Header1
        {}
    """.format(HEADER_CHAR_MAPPER[1] * 7)
    _header_level = 1


@attr.s
class Header2(HeaderLevel):
    """
    Example::

        Header2
        {}
    """.format(HEADER_CHAR_MAPPER[2] * 7)
    _header_level = 2


@attr.s
class Header3(HeaderLevel):
    """
    Example::

        Header3
        {}
    """.format(HEADER_CHAR_MAPPER[3] * 7)
    _header_level = 3


@attr.s
class Header4(HeaderLevel):
    """
    Example::

        Header4
        {}
    """.format(HEADER_CHAR_MAPPER[4] * 7)
    _header_level = 4


@attr.s
class Header5(HeaderLevel):
    """
    Example::

        Header5
        {}
    """.format(HEADER_CHAR_MAPPER[5] * 7)
    _header_level = 5


@attr.s
class Header6(HeaderLevel):
    """
    Example::

        Header6
        {}
    """.format(HEADER_CHAR_MAPPER[6] * 7)
    _header_level = 6


@attr.s
class Header7(HeaderLevel):
    """
    Example::

        Header7
        {}
    """.format(HEADER_CHAR_MAPPER[7] * 7)
    _header_level = 7
