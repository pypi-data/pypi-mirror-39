#/usr/bin/env python
# -*- coding: UTF-8 -*-

from pocoui_lib.crawler.config import KOConfig

class KOBranch(object):
    """
    """
    def __init__(self):
        # 标记
        self.identify = str(KOConfig().increase())
        # 待检索node
        self.node_list = []
        # 完成检索的node
        self.node_traversed_list = []
        # 页面是否可以滑动
        self.can_scroll = False
        # 返回按钮
        self.back_poco = None
        # 某些branch是poco点击后出现的
        self.parent_poco = None
        # 页面类型
        self.branch_type = None

    def back(self):
        """
        点击返回按钮,文字和左上角位置
        """
        pass

    def explore_nodes(self):
        """
        根据一定的规则，遍历node
        """
        pass

    def check_finished(self):
        """
        通过列表和已点击列表对比是否完成检索
        """
        if len(self.node_list) == 0:
            return True
        return False
    def refresh(self):
        """
        页面刷新，重新添加node
        """
        pass
