#/usr/bin/env python
# -*- coding: UTF-8 -*-
from functools import wraps
import yaml

def singleton(cls):
    instances = {}
    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance

@singleton
class KOConfig(object):
    """docstring for .KOConfig"""
    def __init__(self):
        self.config = None
        # branch 自增
        self.increment_num = 0
        # 首页tabbar数组
        self.tabbar_text = []

    def loadDefault(self, filepath):
        with open(filepath, 'r', encoding='utf8') as loadfile:
            self.config = yaml.load(loadfile)
            print(self.config)

    def increase(self):
        self.increment_num = self.increment_num + 1
        return self.increment_num
