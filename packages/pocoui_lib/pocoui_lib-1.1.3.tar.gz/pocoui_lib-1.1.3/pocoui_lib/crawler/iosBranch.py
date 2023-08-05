#/usr/bin/env python
# -*- coding: UTF-8 -*-
from pocoui_lib.crawler.branch import KOBranch
from pocoui_lib.crawler.iosNode import KOIOSNode
from pocoui_lib.crawler.iosNode import KOIOSNodeType
from pocoui_lib.crawler.iosNode import KOIOSNodeAction
from poco.drivers.ios import iosPoco
import logging
import json
import re
poco = iosPoco()
from enum import Enum

class KOIOSBranchType(Enum):
    ReactNative = 1,
    Native = 2,
    WebView = 3,
    NavPage = 4

class KOIOSBranch(KOBranch):
    cell_max_count = 4
    action_node_array = ['Button'];
    scroll_node_array = ['WebView', 'ScrollView', 'Table']

    """
    ios的branch页管理
    """
    def __init__(self):
        KOBranch.__init__(self)
        self.cell_num = 0
        # 事件点击后的回调
        poco.add_post_action_callback(self._action_callback)

        # 默认是rn
        self.branch_type = KOIOSBranchType.ReactNative

    def back(self):
        if self.back_poco:
            if self.back_poco.exists():
                self.back_poco.click()
        elif self.branch_type == KOIOSBranchType.ReactNative:
            poco.click([0.08, 0.06])
        elif self.parent_poco:
            if self.parent_poco.exists():
                self.parent_poco.click()
        else:
            # 如果是弹层，点击位置像是点击两次
            poco.click([0.08, 0.06])

    def check_back_button(self, ui):
        # pos = ui.attr('pos')
        name = ui.attr('name')
        # pattern = re.compile(r"取消|返回|back")
        if 'back' in name:
            self.back_poco = ui
            return True
        else:
            return False

    def explore_nodes(self):
        self.node_list = self.refresh()
        return self.node_list

    def _action_callback(self, poco, action, ui, args):
        # print('[name: %s, type: %s, action: %s]' % (str(ui.attr('name').encode('utf-8')), ui.attr('type'), action))
        #
        # 找到新增的元素，赋值parentpoco
        pass

    def find_root(self):
        # 如果是tabbar要特殊处理
        if poco(type="TabBar"):
            for button in (poco(type="TabBar").child(type="Button")):
                self.node_list.append(KOIOSNode(button))
        return self.node_list

    def refresh(self):
        array_tmp = []
        # print(*poco(), sep='\n')

        for ui in poco():
            # dump出整个UI树
            # print(json.dumps(poco.agent.hierarchy.dump(), indent=2))
            # branch_dict = poco.agent.hierarchy.dumper.dumpHierarchyImpl(root.nodes[0], True)
            node_type = ui.attr('type')
            type = KOIOSNodeType.StaticText
            action = KOIOSNodeAction.click
            # 找到页面id
            if node_type == 'NavigationBar':
                type = KOIOSNodeType.NavigationBar
                if ui.attr('identifier'):
                    self.identify = str(ui.attr('identifier'))
                else:
                    self.identify = str(ui.attr('name'))
                self.branch_type = KOIOSBranchType.Native

            if node_type == 'WebView':
                type = KOIOSNodeType.WebView
                self.branch_type = KOIOSBranchType.WebView

            if node_type in KOIOSBranch.scroll_node_array:
                self.can_scroll = True
            # 将可以点击的点加入到数组中
            if node_type in KOIOSBranch.action_node_array:

                if node_type == 'Button':
                    type = KOIOSNodeType.Button
                    if self.check_back_button(ui):
                        continue
                    # TODO: 排除tabbar的node
                if node_type == 'Cell':
                    self.cell_num = self.cell_num + 1
                    if self.cell_num == KOIOSBranch.cell_max_count:
                        continue
                node = KOIOSNode(ui)
                node.type = type
                node.action = action
                array_tmp.append(node)

        # TODO: 查看当前页面是否有TabBar
        if poco(type="TabBar"):
            for button in poco(type="TabBar").child(type="Button"):
                m = KOIOSNode(button)
                for n in array_tmp:
                    if KOIOSNode.compare(m, n):
                        array_tmp.remove(n)

        return array_tmp
