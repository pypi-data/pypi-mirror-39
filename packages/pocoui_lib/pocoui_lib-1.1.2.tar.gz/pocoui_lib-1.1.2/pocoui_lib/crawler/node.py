#/usr/bin/env python
# -*- coding: UTF-8 -*-

class KONode(object):
    """docstring for node."""
    def __init__(self, poco, parentPoco=None):
        # 当前的poco
        self.poco = poco
        # poco的操作
        self.action = None
        # 当前node的类型
        self.type = None

        self.parent_branch = None

    def trigger_action(self):
        pass
