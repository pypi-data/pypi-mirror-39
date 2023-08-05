# -*- coding: utf-8 -*-

"""
table of content directive.
"""

import attr
from .base import Directive


@attr.s
class TableOfContent(Directive):
    """
    ``.. contents::`` directive.
    """
    title = attr.ib(default=None)
    depth = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(int)),
    )
    local = attr.ib(
        default=False,
        validator=attr.validators.optional(attr.validators.instance_of(bool)),
    )
    backlinks = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )

    meta_directive_keyword = "contents"
    meta_not_none_fields = tuple()

    class BacklinksOptions(object):
        entry = "entry"
        top = "top"
        none = "none"

    @backlinks.validator
    def check_backlinks(self, attribute, value):  # pragma: no cover
        if value not in [None, "entry", "top", "none"]:
            raise ValueError(
                "TableOfContent.backlinks has to be one of 'entry', 'top', 'none'!"
            )

    @property
    def arg(self):
        if self.title is None:
            return ""
        else:
            return self.title
