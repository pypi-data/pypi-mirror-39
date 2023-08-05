#/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from pocoui_lib.crawler.iosBranch import KOIOSBranch
from pocoui_lib.crawler.iosNode import KOIOSNode
from pocoui_lib.crawler.config import KOConfig
import time

class KOPath(object):
    """docstring for Path."""
    def __init__(self):
        # 当前操作的页面
        self.current_branch = None
        # 当前所有page的堆栈
        self._stack = []

    def generate_root(self):
        if KOConfig().config['platform'] == 'ios':
            branch = KOIOSBranch()
            branch.identify = "root"
            branch.find_root()
        return branch

    def check_nodes(self, branch):
        """
        通过node判断是否新建branch，并获取到新建的node, 如果在一个页面上的弹层，暂且看成是两个页面
        """
        if self.current_branch:
            # 如果原生页面的id是一样的
            if (self.current_branch.identify == branch.identify):
                # node的数量不同，就代表是新的页面
                if len(self.current_branch.node_list) != len(branch.node_list):

                    # tmp = []
                    # for m in branch.node_list:
                    #     for n in self.current_branch.node_list:
                    #         if not KOIOSNode.compare(m, n):
                    #             tmp.append(m)
                    branch.node_list = []
                    self.advance_branch(branch)
                    return branch
                # 数量相同代表是同一个页面
                else:
                    return self.current_branch
            else:
                self.advance_branch(branch)
                return branch
        else:
            self.advance_branch(branch)
            return branch


    def explore_branch(self, node=None):
        time.sleep(2)
        # TODO; 判断iOS还是android
        if KOConfig().config['platform'] == 'ios':
            branch = KOIOSBranch()
        branch.explore_nodes()
        branch = self.check_nodes(branch)
        branch.parent_poco = node.poco

        print("=============== branch %s nodes ===================" % (branch.identify))
        print(" || ".join(str(p.poco.attr('name')) for p in branch.node_list))
        print("================================================== \n")

        return branch

    def advance_branch(self, branch):
        """
        加入一个页面
        """
        self._stack.append(branch)
        self.current_branch = branch
        print('enter branch: %s' % (branch.identify))
        self._log_branch_path()

    def back_to_previous_branch(self):
        """
        回到上个页面
        """
        self.current_branch.back()
        # 延时处理
        time.sleep(2)
        self._stack.pop()
        branch = self._stack[-1]

        if (branch):
            self.current_branch = branch
            print('back to branch: %s' % (branch.identify))
            self._log_branch_path()
            return branch
        else:
            return None

    def _log_branch_path(self):
        print("=============== branch path ======================")
        print(" => ".join(str(b.identify) for b in self._stack))
        print("================================================== \n")
