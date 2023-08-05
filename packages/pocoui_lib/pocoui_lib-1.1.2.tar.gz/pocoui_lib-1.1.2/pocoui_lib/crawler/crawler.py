#/usr/bin/env python
# -*- coding: UTF-8 -*-
import yaml
from pocoui_lib.crawler.path import KOPath
from pocoui_lib.crawler.config import KOConfig
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import logging
logging.basicConfig(filename='../log/'+__name__+'.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level = logging.DEBUG,filemode='w',datefmt='%Y-%m-%d %I:%M:%S %p')

class KOCrawler(object):
    """
    node检索，dfs，poco
    """
    def __init__(self, filepath):
        # 路径管理
        self.path = KOPath()
        # 配置信息管理
        KOConfig().loadDefault(filepath)

    def explore(self):
        """
        执行方法
        """
        # 登录操作
        # 到首页的操作，生成tabbar，如果页面里面有tabbar暂时不考虑了
        root = self.path.generate_root()
        self.path.advance_branch(root)
        self.dfs(root)

    def dfs(self, branch):
        """
        遍历branch
        """

        # 判断page是否检索完
        if branch.check_finished():
            print('[branch: %s] explore end \n' % (branch.identify))
            # 回到前一页继续检索
            previous_branch = self.path.back_to_previous_branch()

            if previous_branch:
                self.dfs(previous_branch)
            else:
                return
        for node in branch.node_list:
            # 找到没有检索的node继续检索
            if node not in branch.node_traversed_list:
                branch.node_traversed_list.append(node)
                branch.node_list.remove(node)
                node.trigger_action()
                print('[node: %s, pos:%s] action end \n' % (node.poco.attr('name'), node.poco.attr('pos')))
                self.dfs(self.path.explore_branch(node))
