#/usr/bin/env python
# -*- coding: UTF-8 -*-

from pocoui_lib.crawler.node import KONode
from enum import Enum
import time

class KOIOSNodeType(Enum):
    Application = 0
    Window = 1
    NavigationBar = 2
    TabBar = 3
    ScrollView = 4
    WebView = 5
    Table = 6
    Cell = 7
    StaticText = 8
    TextField = 9
    Button = 10
    Image = 11

class KOIOSNodeAction(Enum):
    click = 1

class KOIOSNode(KONode):
    """docstring for Page."""

    @classmethod
    def compare(cls, node, anothernode):
        if (node.poco.attr('name') == anothernode.poco.attr('name')):
        # and (node.poco.attr('pos') == anothernode.poco.attr('pos')):
            return True
        else:
            return False

    def trigger_action(self):
        time.sleep(2)
        if self.poco.exists:
            if self.action == KOIOSNodeAction.click:
                self.poco.click()
