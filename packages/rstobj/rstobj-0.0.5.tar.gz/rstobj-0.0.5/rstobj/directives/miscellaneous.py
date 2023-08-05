# -*- coding: utf-8 -*-

"""

"""

import attr
from .base import Directive


@attr.s
class Include(Directive):
    """
    ``.. include::`` directive.
    """
    path = attr.ib(default=None)
    start_line = attr.ib(default=None)
    end_line = attr.ib(default=None)
    start_after = attr.ib(default=None)
    end_before = attr.ib(default=None)
    literal = attr.ib(default=None)
    code = attr.ib(default=None)
    number_lines = attr.ib(default=None)
    encoding = attr.ib(default=None)
    tab_width = attr.ib(default=None)

    meta_directive_keyword = "include"
    meta_not_none_fields = ("path",)

    @property
    def arg(self):
        return self.path
