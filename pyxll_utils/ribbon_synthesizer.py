#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import logging
import os
import sys
from collections import OrderedDict

from lxml import etree


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring  # noqa


logging.basicConfig(
    format='%(asctime)s %(levelname)-8.8s [%(name)s:%(lineno)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level='INFO')
logger = logging.getLogger(__name__)


EMPTY_RIBBON = '''\
<customUI xmlns="http://schemas.microsoft.com/office/2006/01/customui"
          loadImage="pyxll.load_image">  <!-- pyxll.load_image is a built-in image loader -->
    <ribbon>
        <tabs>
        </tabs>
    </ribbon>
</customUI>'''  # noqa

SAMPLE_RIBBON_FRAGMENT = '''\
<tab id="pyxll_example_tab">
    <group id="foo">
        <button>foo</button>
    </group>
</tab>'''


class RibbonSynthesizer(object):

    @classmethod
    def from_file(cls, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                default_ribbon = f.read()
        else:
            default_ribbon = None
        return cls(default_ribbon=default_ribbon)

    def __init__(self, default_ribbon=None):
        self.ribbon = default_ribbon or EMPTY_RIBBON
        self._elements_to_insert = OrderedDict()

    def to_bytes(self, names=None):
        if names is None:
            names = sorted(self._elements_to_insert.keys())
        ribbon = self.parse(self.ribbon)
        tabs = self.get_tabs(ribbon)
        for name in names:
            try:
                tab = self._elements_to_insert[name]
            except KeyError:
                logger.info("skip {}".format(name))
                # This isn't an error. It probably just means that the
                # requested extension didn't submit a fragment.
                continue
            self.upsert_by_attribute(tabs, tab)
        return self.element_as_bytes(ribbon)

    @staticmethod
    def parse(buf):
        return etree.fromstring(buf)

    @staticmethod
    def element_as_bytes(element):
        return etree.tostring(element, pretty_print=True)

    @staticmethod
    def get_tabs(root):
        return root.find('.//{*}ribbon/{*}tabs')

    def submit_ribbon_tab(self, extension_name, tab_buffer):
        root_elem = self.parse(tab_buffer)
        if root_elem.tag != 'tab':
            msg = ("Ignoring fragment {}:\n{}\n"
                   "Ribbons must be <tab> elements like this:\n{}")
            logger.warning(
                msg.format(extension_name, tab_buffer, SAMPLE_RIBBON_FRAGMENT))
            return
        else:
            logger.info("Adding ribbon fragment: {}".format(extension_name))
            self._elements_to_insert[extension_name] = root_elem

    @staticmethod
    def upsert_by_attribute(parent, element, attr='id'):
        """Add or append `element` to parent depending on `attr`.

        If `parent` contains a child such that:
            (element.tag, element.get(attr)) == (child.tag, child.get(attr))
        then we add the contents of element to child.
        Otherwise, we add element as a sibling of child.

        This allows us to extend existing elements by matching on attr.
        """

        tag = element.tag
        attr_val = element.get(attr)
        query = '{tag}[@{attr}="{attr_val}"]'.format(**locals())
        matches = parent.findall("{*}" + query)
        if matches:
            match = matches[0]
            match.extend(element.getchildren())
        else:
            parent.append(element)
        return parent
